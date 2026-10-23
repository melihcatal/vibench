from google.cloud import translate_v3 as translate
import os


def translate_text(text: str, target_language: str, project_id: str):
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    location = "global"  # For global endpoint
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    TEXT_TO_TRANSLATE = "Hello, world!"
    TARGET_LANGUAGE = "es"  # e.g., "es" for Spanish

    if PROJECT_ID:
        translated_output = translate_text(
            TEXT_TO_TRANSLATE, TARGET_LANGUAGE, PROJECT_ID
        )
        print(f"Original: {TEXT_TO_TRANSLATE}")
        print(f"Translated ({TARGET_LANGUAGE}): {translated_output}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT.")
