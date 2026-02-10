import json
import uuid
import re
from sentence_transformers import SentenceTransformer

LOG_FILE_PATH = r"C:\Users\User\Desktop\lograg\sample_logs\app.log"
OUTPUT_FILE = r"C:\Users\User\Desktop\lograg\data\logs_vectors.jsonl"

model = SentenceTransformer("all-MiniLM-L6-v2")

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<service>[\w\-]+)\s+"
    r"(?P<message>.*)"
)


def parse_logs(path):
    events = []
    current = None

    with open(path, "r", encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.strip()

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
    """
    Build a rich semantic document for embedding.
    This dramatically improves retrieval quality.
    """

    text = f"""
Source: application-log
Service: {event['service']}
Layer: application
Level: {event['level']}
Timestamp: {event['timestamp']}

Message:
{event['message']}

Stack Trace:
{event.get('stack', '')}
""".strip()

    return model.encode(text).tolist()



def main():
    events = parse_logs(LOG_FILE_PATH)
    print(f"Parsed {len(events)} events")

    if not events:
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for event in events:
            record = {
                "id": str(uuid.uuid4()),
                "vector": embed_event(event),
                "metadata": event
            }
            out.write(json.dumps(record) + "\n")

    print(f"Wrote vectors to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
