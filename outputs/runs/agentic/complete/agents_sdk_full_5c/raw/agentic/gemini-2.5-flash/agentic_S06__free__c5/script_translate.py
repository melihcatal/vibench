
from google.cloud import translate_v2 as translate
import os

def translate_script(text: str, target_language_code: str, source_language_code: str = None) -> str:
    """Translates narration script text using Google Cloud Translation V2 API."""
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case translation will be done per string
    result = translate_client.translate(
        text,
        target_language=target_language_code,
        source_language=source_language_code,
    )

    translated_text = result["translatedText"]
    print(f"Translated '{text[:30]}...' to '{translated_text[:30]}...'")
    return translated_text

if __name__ == '__main__':
    original_script = "Hello team, this is an important message about our new project launch."
    target_lang = "es"
    translated_script = translate_script(original_script, target_lang, source_language_code="en")
    print(f"Original: {original_script}")
    print(f"Translated ({target_lang}): {translated_script}")

    original_script_jp = "こんにちは、チームの皆さん、新しいプロジェクトの立ち上げに関する重要なお知らせです。"
    target_lang_en = "en"
    translated_script_en = translate_script(original_script_jp, target_lang_en, source_language_code="ja")
    print(f"Original: {original_script_jp}")
    print(f"Translated ({target_lang_en}): {translated_script_en}")
