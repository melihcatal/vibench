from observability_client import get_translation_client


def translate_log_message(text: str, target_language: str = "es") -> str:
    translate_client = get_translation_client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
