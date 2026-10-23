import boto3
import os
from database_models import Document


def translate_user_facing_document_fields(
    document: Document, target_language_code: str = "es"
) -> Document:
    translate_client = boto3.client(
        "translate", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    translated_doc = {}
    for key, value in document.items():
        if isinstance(value, str):
            response = translate_client.translate_text(
                Text=value,
                SourceLanguageCode="auto",
                TargetLanguageCode=target_language_code,
            )
            translated_doc[key] = response["TranslatedText"]
        else:
            translated_doc[key] = value
    return translated_doc
