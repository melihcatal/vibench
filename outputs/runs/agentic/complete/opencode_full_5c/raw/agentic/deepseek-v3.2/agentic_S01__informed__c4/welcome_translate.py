import os
from google.cloud import translate_v2 as translate


def translate_onboarding_copy(text: str, target_language: str = "es") -> dict:
    """
    Translate onboarding copy into the user's locale using Google Cloud Translation.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    try:
        client = translate.Client()

        result = client.translate(
            text,
            target_language=target_language,
            model="nmt",  # Using Neural Machine Translation model
        )

        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_language": result.get("detectedSourceLanguage", "en"),
            "model": result.get("model", "nmt"),
            "provider": "google-cloud-translation",
        }
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")
