from google.cloud import translate_v2 as translate


def translate_script(script: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(script, target_language=target_language)
    return result["translatedText"]
