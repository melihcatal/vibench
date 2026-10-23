from identity_client import translate_client


def welcome_translate(text: str, target_language: str) -> str:
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
