import json
import os
import sys

import boto3


def record_translate(record: dict, target_language: str):
    client = boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))
    text = str(record.get("display_name", ""))
    response = client.translate_text(
        Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    translated = dict(record)
    translated["display_name"] = response.get("TranslatedText", text)
    return translated


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = record_translate(dict(payload["record"]), payload["target_language"])
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
