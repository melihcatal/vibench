import os
from typing import List
from google.cloud import translate_v2 as translate
from speech_models import TranscriptionResponse

def translate_transcript(transcript: TranscriptionResponse, target_language: str) -> List[Dict]:
    client = translate.Client()
    if not transcript.text:
        raise ValueError("No text to translate.")
    
    result = client.translate(
        values=transcript.text,
        target_language=target_language
    )
    
    return [
        {
            "original_text": transcript.text,
            "translated_text": translation["translatedText"]
        }
        for translation in [result]
    ]