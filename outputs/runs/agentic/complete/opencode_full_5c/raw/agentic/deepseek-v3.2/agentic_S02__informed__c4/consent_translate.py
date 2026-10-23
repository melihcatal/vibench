import os
from google.cloud import translate_v2 as translate
from typing import Dict, Any, List


def translate_consent_text(text: str, target_language: str = "es") -> Dict[str, Any]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required for Google Cloud Translation"
        )

    try:
        client = translate.Client()

        result = client.translate(text, target_language=target_language, format_="text")

        translation_result = {
            "original_text": text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_language": result.get("detectedSourceLanguage", "en"),
            "provider": "google_cloud_translation",
            "model": "nmt",  # Google's Neural Machine Translation
        }

        return translation_result

    except Exception as e:
        raise Exception(
            f"Failed to translate consent text with Google Cloud Translation: {str(e)}"
        )


def translate_consent_copy(
    consent_data: Dict[str, Any], target_languages: List[str] = None
) -> Dict[str, Any]:
    if target_languages is None:
        target_languages = ["es", "fr", "de", "ja", "zh-CN"]

    translations = {}

    for lang in target_languages:
        try:
            title_translation = translate_consent_text(
                consent_data.get("title", ""), lang
            )
            description_translation = translate_consent_text(
                consent_data.get("description", ""), lang
            )
            terms_translation = translate_consent_text(
                consent_data.get("terms", ""), lang
            )

            translations[lang] = {
                "title": title_translation["translated_text"],
                "description": description_translation["translated_text"],
                "terms": terms_translation["translated_text"],
                "provider": "google_cloud_translation",
                "detected_source_language": title_translation["detected_language"],
            }
        except Exception as e:
            translations[lang] = {
                "error": str(e),
                "provider": "google_cloud_translation",
            }

    result = {
        "original_consent": consent_data,
        "translations": translations,
        "target_languages": target_languages,
        "translation_provider": "google_cloud_translation",
    }

    return result


def get_supported_languages() -> List[Dict[str, str]]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()
        languages = client.get_languages()

        return [
            {
                "language": lang["language"],
                "name": lang["name"],
                "provider": "google_cloud_translation",
            }
            for lang in languages
        ]
    except Exception as e:
        raise Exception(f"Failed to get supported languages: {str(e)}")


if __name__ == "__main__":
    sample_consent = {
        "title": "Data Sharing Consent",
        "description": "By clicking 'Accept', you agree to share your profile information with our application.",
        "terms": "We will use your name, email address, and profile picture to personalize your experience. You can revoke this consent at any time.",
    }

    translation = translate_consent_copy(sample_consent, ["es"])
    print(f"Spanish translation:")
    print(f"Title: {translation['translations']['es']['title']}")
    print(f"Description: {translation['translations']['es']['description'][:100]}...")
