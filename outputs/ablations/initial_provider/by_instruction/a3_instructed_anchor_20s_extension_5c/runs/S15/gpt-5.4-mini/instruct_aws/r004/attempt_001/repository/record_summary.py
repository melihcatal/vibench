import json
import os


def record_summary(record):
    text = record if isinstance(record, str) else json.dumps(record, ensure_ascii=False)
    return {"summary": text[:200]}


def main():
    print(json.dumps(record_summary(os.environ.get("RECORD_JSON", "{}"))))


if __name__ == "__main__":
    main()
