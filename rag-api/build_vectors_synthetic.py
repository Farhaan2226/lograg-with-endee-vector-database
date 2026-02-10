import json
import uuid
from sentence_transformers import SentenceTransformer

INPUT_FILE = r"C:\Users\User\Desktop\lograg\ingestion\synthetic_logs.json"
OUTPUT_FILE = r"C:\Users\User\Desktop\lograg\data\logs_index\data.jsonl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_log(log):
    """
    Build rich semantic text for embedding
    """

    text = f"""
Source: {log.get('source', 'unknown')}
Service: {log.get('service', 'unknown')}
Component: {log.get('component', '')}
Layer: {log.get('layer', '')}
Level: {log.get('level', '')}
Host: {log.get('host', '')}
Timestamp: {log.get('timestamp', '')}
Tags: {' '.join(log.get('tags', []))}

Message:
{log.get('message', '')}

Stack Trace:
{log.get('stack', '')}
""".strip()

    return model.encode(text).tolist()


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)

    print(f"Loaded {len(logs)} synthetic logs")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for log in logs:
            record = {
                "id": str(uuid.uuid4()),
                "vector": embed_log(log),
                "metadata": log
            }
            out.write(json.dumps(record) + "\n")

    print(f"Wrote vectors → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
