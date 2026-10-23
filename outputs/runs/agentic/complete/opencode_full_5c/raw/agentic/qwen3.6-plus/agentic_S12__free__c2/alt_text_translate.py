import os
from typing import Optional, List
import boto3
from botocore.config import Config

from describe_image import describe_image, ImageDescriptionResponse


AWS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_TRANSLATE_ENDPOINT = os.environ.get("AWS_TRANSLATE_ENDPOINT", None)

_translate_client = None


def get_translate_client() -> boto3.client:
    global _translate_client

    if _translate_client is not None:
        return _translate_client

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
        connect_timeout=30,
    )

    kwargs = {"config": config}
    if AWS_TRANSLATE_ENDPOINT:
        kwargs["endpoint_url"] = AWS_TRANSLATE_ENDPOINT

    _translate_client = session.client("translate", **kwargs)
    return _translate_client


def translate_text(
    text: str, source_language: str = "en", target_language: str = "es"
) -> str:
    client = get_translate_client()

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    return response.get("TranslatedText", text)


def alt_text_translate(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    target_languages: Optional[List[str]] = None,
    source_language: str = "en",
) -> dict:
    if target_languages is None:
        target_languages = ["es", "fr", "de", "ja", "zh"]

    description_result = describe_image(
        image_path=image_path,
        image_bytes=image_bytes,
        max_descriptions=3,
    )

    translations = {}
    for lang in target_languages:
        translated_descriptions = []
        for desc in description_result.descriptions:
            translated = translate_text(
                text=desc,
                source_language=source_language,
                target_language=lang,
            )
            translated_descriptions.append(translated)
        translations[lang] = translated_descriptions

    return {
        "source_language": source_language,
        "original_descriptions": description_result.descriptions,
        "translations": translations,
        "model": "aws-translate-text-v3",
        "vision_model": description_result.model,
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python alt_text_translate.py <image_path> [lang1 lang2 ...]")
        sys.exit(1)

    langs = sys.argv[2:] if len(sys.argv) > 2 else None
    result = alt_text_translate(image_path=sys.argv[1], target_languages=langs)
    print(json.dumps(result, indent=2, ensure_ascii=False))
