from google.cloud import translate_v2 as translate


def translate_transcript(transcript: str, target_language: str = "es") -> str:
    client = translate.Client()
    result = client.translate(transcript, target_language=target_language)
    return result["translatedText"]
