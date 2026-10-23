import os
from google.cloud import translate_v2 as translate
import text_to_speech

def generate_localized_audio_preview(text, target_language):
    client = translate.Client()
    translated_text = client.translate(text, target_language=target_language)['translatedText']
    audio = text_to_speech.synthesize(translated_text, target_language)
    return audio