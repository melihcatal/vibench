import boto3
import os


def translate_result(payload, config=None):
    config = config or {}
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("translate", region_name=aws_region)

    text_to_translate = payload["text"]
    target_language_code = payload.get("target_language", "en")
    source_language_code = payload.get("source_language", "auto")

    if source_language_code == "auto":
        response = client.translate_text(
            Text=text_to_translate,
            TargetLanguageCode=target_language_code
        )
    else:
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )

    translated_text = response["TranslatedText"]
    return {"translated_text": translated_text, "source_language": response.get("SourceLanguageCode"), "target_language": target_language_code}
