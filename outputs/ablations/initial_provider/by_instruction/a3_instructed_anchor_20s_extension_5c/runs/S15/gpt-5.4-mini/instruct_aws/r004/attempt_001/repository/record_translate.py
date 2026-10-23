import json
import os

import boto3


def record_translate(text, source_language, target_language):
    client = boto3.client("translate", region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText")}


def main():
    print(json.dumps(record_translate(os.environ.get("RECORD_TEXT", ""), os.environ.get("SOURCE_LANGUAGE", "en"), os.environ.get("TARGET_LANGUAGE", "es"))))


if __name__ == "__main__":
    main()
