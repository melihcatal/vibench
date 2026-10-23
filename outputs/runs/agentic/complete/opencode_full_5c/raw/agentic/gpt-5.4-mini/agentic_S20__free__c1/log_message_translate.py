import os

from google.cloud import translate_v3 as translate


def translate_message(text: str, target_language: str = "es") -> dict:
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(
        contents=[text], target_language_code=target_language, parent=parent
    )
    return {
        "translated_text": response.translations[0].translated_text
        if response.translations
        else ""
    }


if __name__ == "__main__":
    translate_message("")
