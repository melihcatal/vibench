from google.cloud import translate_v2 as translate


def translate_script(script: str, target_language: str = "en") -> str:
    client = translate.Client()
    translation = client.translate(script, target_language=target_language)
    return translation["translatedText"]
