from google.cloud import translate_v2 as translate


def translate_transcript(text, target_language, config=None):
    config = config or {}
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
