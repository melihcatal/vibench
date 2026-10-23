import os
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def get_speech_client():
    return DeepgramClient(DEEPGRAM_API_KEY)

def get_live_options(model='nova-2', language='en-US', punctuate=True, interim_results=True):
    return LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
    )