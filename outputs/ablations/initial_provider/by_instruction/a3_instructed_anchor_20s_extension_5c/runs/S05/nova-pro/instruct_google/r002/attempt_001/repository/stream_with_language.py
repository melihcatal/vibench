from speech_client import speech_client
from speech_models import create_streaming_request
from google.cloud.speech import enums

# Start a streaming recognizer with language and punctuation settings
def stream_with_language(language_code='en-US'):
    config = types.StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True),
        interim_results=True)
    for audio_content in stream_microphone():
        request = create_streaming_request(config, audio_content)
        responses = speech_client.streaming_recognize(request)
        partial_results(responses)