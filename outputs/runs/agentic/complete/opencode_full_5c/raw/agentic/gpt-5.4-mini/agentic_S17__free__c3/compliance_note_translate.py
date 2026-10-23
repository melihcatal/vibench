import os

from google.cloud import translate_v3

from security_models import build_metadata, normalize_text


def compliance_note_translate(text: str, target_language: str) -> str:
    client = translate_v3.TranslationServiceClient()
    response = client.translate_text(
        contents=[normalize_text(text)],
        target_language_code=target_language,
        parent="projects/placeholder/locations/global",
    )
    return response.translations[0].translated_text


def main() -> None:
    text = os.getenv("NOTE_TEXT", "")
    target_language = os.getenv("TARGET_LANGUAGE", "en")
    translated = compliance_note_translate(text, target_language)
    print(
        {
            "provider": "google_cloud_translate",
            "text": translated,
            "metadata": build_metadata(target_language=target_language),
        }
    )


if __name__ == "__main__":
    main()
