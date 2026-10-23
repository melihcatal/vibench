from google.cloud import translate_v2 as translate

from speech_models import TranslationRequest, normalize_transcript_text


def translate_transcript(transcript, target_language: str):
    client = translate.Client()
    text = normalize_transcript_text(transcript)
    request = TranslationRequest(text=text, target_language=target_language)
    return client.translate(request.text, target_language=request.target_language)
