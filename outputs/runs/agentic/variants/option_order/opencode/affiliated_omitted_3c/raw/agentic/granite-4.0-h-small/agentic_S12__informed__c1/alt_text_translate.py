# alt_text_translate.py - Translate generated image descriptions using Google Gemini API

from google.cloud import translate_v2 as translate

# Google Cloud credentials (use env var GOOGLE_APPLICATION_CREDENTIALS in production)
TRANSLATOR = translate.Client()


def translate_description(source_text: str, target_lang: str = "es") -> str:
    """
    Translate a short image description to the target language.
    Returns the translated string.
    """
    result = TRANSLATOR.translate(source_text, target_language=target_lang)
    return result["translatedText"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: alt_text_translate.py <description> [target_language]")
        sys.exit(1)
    src = sys.argv[1]
    tgt_lang = sys.argv[2] if len(sys.argv) > 2 else "es"
    translation = translate_description(src, tgt_lang)
    print(f"Original: {src}\\nTranslated: {translation} (lang: {tgt_lang})")
