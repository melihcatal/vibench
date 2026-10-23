from speech_client import speech_to_text
from speech_models import normalize_transcript

def stream_with_language(language='en-US', punctuation=True):
    with speech_to_text.create_session(config={'language_customization_id': language, 'smart_formatting': punctuation}) as session:
        while True:
            audio_data = input('Enter audio data (or type 