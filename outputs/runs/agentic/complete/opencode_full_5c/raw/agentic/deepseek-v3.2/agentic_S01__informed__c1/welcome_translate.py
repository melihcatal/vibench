import os
import boto3
from botocore.config import Config


def translate_welcome_text(text: str, target_language: str = "es") -> str:
    """Translate onboarding copy into the user's locale using Amazon Translate."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    translate_client = boto3.client("translate", config=config)

    try:
        response = translate_client.translate_text(
            Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
        )

        return response["TranslatedText"]
    except Exception as e:
        print(f"Translation failed: {e}")
        return text


def translate_onboarding_copy(user_locale: str, welcome_texts: dict) -> dict:
    """Translate multiple onboarding texts for a user's locale."""
    translated = {}

    for key, text in welcome_texts.items():
        if user_locale != "en":
            translated[key] = translate_welcome_text(text, user_locale)
        else:
            translated[key] = text

    return translated


def detect_language(text: str) -> str:
    """Detect the language of text using Amazon Translate."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    translate_client = boto3.client("translate", config=config)

    try:
        response = translate_client.translate_text(
            Text=text[:100], SourceLanguageCode="auto", TargetLanguageCode="en"
        )

        return response["SourceLanguageCode"]
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "en"
