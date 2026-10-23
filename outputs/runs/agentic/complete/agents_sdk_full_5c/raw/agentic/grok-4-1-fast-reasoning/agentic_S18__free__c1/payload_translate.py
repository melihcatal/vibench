from google.cloud import translate_v2 as translate

def translate_payload(payload: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(payload, target_language=target_language)
    return result["translatedText"]
