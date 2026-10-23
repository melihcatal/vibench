from google.cloud import translate_v2 as translate


def translate_dashboard_note(text: str, target_language: str) -> str:
    try:
        translate_client = translate.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language=target_language)

        return result["translatedText"]
    except Exception as e:
        return f"An error occurred during translation: {e}"
