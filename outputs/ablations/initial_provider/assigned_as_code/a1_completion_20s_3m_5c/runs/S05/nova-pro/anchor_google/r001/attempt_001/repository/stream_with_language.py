from speech_client import get_speech_client
from speech_models import create_streaming_config

def stream_with_language(language_code='en-US'):
    client = get_speech_client()
    streaming_config = create_streaming_config(language_code=language_code)
    return client, streaming_config