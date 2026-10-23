import os
from typing import Optional, List, Dict, Any

import boto3


def stored_text_translate(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    terminology_names: Optional[List[str]] = None,
) -> Dict[str, Any]:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    translate_kwargs = {
        "Text": text,
        "SourceLanguageCode": source_language,
        "TargetLanguageCode": target_language,
    }

    if terminology_names:
        translate_kwargs["TerminologyNames"] = terminology_names

    try:
        response = translate_client.translate_text(**translate_kwargs)

        translated_text = response.get("TranslatedText", "")
        detected_source = response.get("SourceLanguageCode", source_language)

        return {
            "success": True,
            "original_text": text,
            "translated_text": translated_text,
            "source_language": detected_source,
            "target_language": target_language,
            "terminology_applied": terminology_names if terminology_names else [],
        }
    except Exception as exc:
        return {
            "success": False,
            "original_text": text,
            "error": str(exc),
            "source_language": source_language,
            "target_language": target_language,
        }
