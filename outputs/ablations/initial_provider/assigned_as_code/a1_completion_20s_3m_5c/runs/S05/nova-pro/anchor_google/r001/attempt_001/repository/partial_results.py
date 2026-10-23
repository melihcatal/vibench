from speech_client import get_speech_client
from speech_models import create_streaming_config

def partial_results(response):
    for result in response.results:
        if not result.is_final:
            yield result.alternatives[0].transcript
        else:
            yield result.alternatives[0].transcript