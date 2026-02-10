import uuid
import re
import requests
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ----------------

ENDEE_BASE_URL = "http://localhost:8080"
INDEX_NAME = "logs_index"
EMBEDDING_DIM = 384
LOG_FILE_PATH = r"C:\Users\User\Desktop\lograg\sample_logs\app.log"

# ---------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<service>[\w\-]+)\s+"
    r"(?P<message>.*)"
)


def parse_logs(file_path):
    events = []
    current = None

    # utf-8-sig handles Windows BOM correctly
    with open(file_path, "r", encoding="utf-8-sig") as f:
        for raw_line in f:
            line = raw_line.strip()

            match = LOG_PATTERN.match(line)
            if match:
                if current:
                    events.append(current)

                current = {
                    "timestamp": f"{match.group('date')} {match.group('time')}",
                    "level": match.group("level"),
                    "service": match.group("service"),
                    "message": match.group("message"),
                    "stack": ""
                }
            elif current and line:
                current["stack"] += line + "\n"

        if current:
            events.append(current)

    return events


def embed_event(event):
    text = (
        f"[{event['level']}] {event['service']}\n"
        f"{event['message']}\n"
        f"{event['stack']}"
    )
    return model.encode(text).tolist()


def upsert_event(event):
    vector = embed_event(event)

    payload = [
        {
            "id": str(uuid.uuid4()),
            "vector": vector,
            "metadata": {
                "service": event["service"],
                "level": event["level"],
                "timestamp": event["timestamp"],
                "message": event["message"]
            }
        }
    ]

    url = f"{ENDEE_BASE_URL}/api/v1/index/{INDEX_NAME}/upsert"
    response = requests.put(url, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"Upsert failed ({response.status_code}): {response.text}"
        )


def main():
    events = parse_logs(LOG_FILE_PATH)
    print(f"Parsed {len(events)} events")

    if not events:
        print("No events found — stopping.")
        return

    for event in events:
        upsert_event(event)

    print(f"Ingested {len(events)} log events into Endee.")


if __name__ == "__main__":
    main()
