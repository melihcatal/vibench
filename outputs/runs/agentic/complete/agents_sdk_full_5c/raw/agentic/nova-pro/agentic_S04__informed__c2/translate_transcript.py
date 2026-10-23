import os
from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_transcript(transcript_text, target_language='en'):
    translation = client.translate(transcript_text, target_language=target_language)
    return translation['translatedText']