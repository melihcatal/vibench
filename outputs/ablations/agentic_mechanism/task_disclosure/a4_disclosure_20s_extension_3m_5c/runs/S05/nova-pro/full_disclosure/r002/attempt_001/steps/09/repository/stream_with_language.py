import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Set environment variables for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

def stream_with_language(language_code, enable_automatic_punctuation):
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # Simulate streaming recognition
    # In a real application, you would yield audio data from a stream
    # For demonstration, we use a placeholder
    audio_generator = [b'This is a test audio stream.']

    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

# Example usage
# stream_with_language('en-US', True)