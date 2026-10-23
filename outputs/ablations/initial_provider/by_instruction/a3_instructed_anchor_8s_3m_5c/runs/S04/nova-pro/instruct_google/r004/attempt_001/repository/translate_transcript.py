from google.cloud import translate
from speech_models import TranscriptionResponse

def translate_transcript(transcription_response, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = transcription_response.response
    translated_text = client.translate_text(parent, response.results[0].alternatives[0].transcript, target_language).translated_text
    return translated_text