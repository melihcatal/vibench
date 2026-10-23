import json
import os
import sys

import boto3


def record_text_safety(record: dict):
    client = boto3.client(
        "comprehend", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    text = str(record.get("text", ""))[:5000]
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    unsafe = any(
        entity.get("Type") in {"SSN", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER"}
        for entity in response.get("Entities", [])
    )
    return {"document_id": record.get("document_id"), "unsafe": unsafe}


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = record_text_safety(dict(payload["record"]))
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
