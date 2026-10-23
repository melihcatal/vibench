from google.cloud import translate_v2 as translate
import os


def translate_text(text: str, target_language: str, project_id: str):
    translate_client = translate.Client(project=project_id)
    response = translate_client.translate(text, target_language=target_language)
    translated_text = response["translatedText"]
    source_language = response["detectedSourceLanguage"]
    return translated_text, source_language


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if project_id:
        text_to_translate = "The quick brown fox jumps over the lazy dog."
        target_lang = "es"
        print(f"Translating '{text_to_translate}' to {target_lang}...")
        translated, source = translate_text(text_to_translate, target_lang, project_id)
        print(f"Source Language: {source}")
        print(f"Translated Text: {translated}")

        text_to_translate_japanese = "こんにちは世界"
        target_lang_english = "en"
        print(
            f"\nTranslating '{text_to_translate_japanese}' to {target_lang_english}..."
        )
        translated_eng, source_jp = translate_text(
            text_to_translate_japanese, target_lang_english, project_id
        )
        print(f"Source Language: {source_jp}")
        print(f"Translated Text: {translated_eng}")
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID environment variable and ensure GOOGLE_APPLICATION_CREDENTIALS is set."
        )
