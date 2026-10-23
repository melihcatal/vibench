import boto3
import os


def translate_compliance_note(payload, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")

    translate_client = boto3.client("translate", region_name=region_name)

    text = payload["text"]
    source_language_code = payload.get("source_language_code", "auto")
    target_language_code = payload["target_language_code"]

    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    return {"translated_text": response["TranslatedText"], "source_language_code": response["SourceLanguageCode"]}
