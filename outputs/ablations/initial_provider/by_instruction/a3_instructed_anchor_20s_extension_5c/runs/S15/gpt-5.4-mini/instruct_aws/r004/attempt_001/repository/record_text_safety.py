import json
import os

import boto3


def record_text_safety(text):
    client = boto3.client("comprehend", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1")
    response = client.detect_dominant_language(Text=text[:5000])
    return {"languages": response.get("Languages", [])}


def main():
    print(json.dumps(record_text_safety(os.environ.get("RECORD_TEXT", ""))))


if __name__ == "__main__":
    main()
