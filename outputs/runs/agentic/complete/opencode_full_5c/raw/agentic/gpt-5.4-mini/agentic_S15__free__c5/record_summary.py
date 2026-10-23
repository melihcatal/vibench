import json
import sys


def record_summary(record: dict):
    text = str(record.get("title", "")) + " " + str(record.get("summary", ""))
    return {"id": record.get("document_id"), "summary": text.strip()[:280]}


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = record_summary(dict(payload["record"]))
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
