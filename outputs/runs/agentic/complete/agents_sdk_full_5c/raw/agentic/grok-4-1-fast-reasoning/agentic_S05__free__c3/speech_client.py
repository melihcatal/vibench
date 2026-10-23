import os
from deepgram import DeepgramClient, LiveOptions

def get_stt_client():
    api_key = os.getenv('DEEPGRAM_API_KEY')
    if not api_key:
        raise ValueError('DEEPGRAM_API_KEY environment variable is required.')
    return DeepgramClient(api_key)

def get_live_options(
    model='nova-2',
    language='en',
    punctuate=True,
    interim_results=True,
    smart_format=True
):
    return LiveOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        interim_results=interim_results,
        smart_format=smart_format
    )