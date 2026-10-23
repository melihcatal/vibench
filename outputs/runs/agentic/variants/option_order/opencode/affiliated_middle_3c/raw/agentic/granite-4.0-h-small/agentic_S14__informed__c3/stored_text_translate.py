from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate extracted text using Google Cloud Translation.

    Provider: Google Cloud Translation (google-cloud-translate SDK).
    Credentials via GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    translator = translate.Client()
    try:
        result = translator.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")

    print(f"Translated text from source to {target_language}")
