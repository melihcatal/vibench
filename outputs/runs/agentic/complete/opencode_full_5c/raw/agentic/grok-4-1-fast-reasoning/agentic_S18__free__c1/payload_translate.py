from google.cloud import translate_v2 as translate

translator = translate.Client()


def translate_payload_text(text: str, target_language: str = "es") -> str:
    if not text:
        return ""
    result = translator.translate(text, target_language=target_language)
    return result["translatedText"]
