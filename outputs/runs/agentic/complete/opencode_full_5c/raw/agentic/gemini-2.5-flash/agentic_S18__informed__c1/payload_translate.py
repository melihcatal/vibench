import os
import boto3
from messaging_models import TranslatedPayload


def translate_payload_text(
    text: str, target_language_code: str, source_language_code: str = "auto"
) -> TranslatedPayload:
    translate_client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    if source_language_code == "auto":
        response = translate_client.translate_text(
            Text=text, TargetLanguageCode=target_language_code
        )
        actual_source_language = response.get("SourceLanguageCode", "unknown")
    else:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        actual_source_language = source_language_code

    return TranslatedPayload(
        translated_text=response["TranslatedText"],
        source_language=actual_source_language,
        target_language=target_language_code,
    )
