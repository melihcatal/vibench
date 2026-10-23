from google.cloud import translate_v2 as translate

from speech_models import normalize_transcript


def live_caption_translate(text: str, target_language: str):
    client = translate.Client()
    response = client.translate(
        normalize_transcript(text), target_language=target_language
    )
    return response["translatedText"]
