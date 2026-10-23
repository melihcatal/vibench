from google.cloud import speech
from speech_client import create_speech_client
from speech_models import create_streaming_config, normalize_streaming_response

def stream_chunks():
    client = create_speech_client()
    config = create_streaming_config()
    streaming_config = speech.StreamingRecognizeRequest(streaming_config=config)
    yield streaming_config

    # Simulate streaming audio chunks
    for i in range(5):
        audio_content = b'simulated_audio_chunk'
        audio = speech.RecognitionAudio(content=audio_content)
        request = speech.StreamingRecognizeRequest(audio_content=audio)
        yield request

def partial_results(response):
    return normalize_streaming_response(response)

def stream_with_language(language_code='en-US'):
    client = create_speech_client()
    config = create_streaming_config(language_code=language_code)
    streaming_config = speech.StreamingRecognizeRequest(streaming_config=config)
    response = client.streaming_recognize([streaming_config])
    return partial_results(response)