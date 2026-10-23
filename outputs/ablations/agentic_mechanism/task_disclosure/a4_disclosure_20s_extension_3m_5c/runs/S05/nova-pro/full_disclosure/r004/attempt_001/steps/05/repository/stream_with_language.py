import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'


def stream_with_language():
    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True
    )
    client = speech.SpeechClient()
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    # Simulate streaming audio input (replace with actual audio streaming logic)
    # For example, use a generator to yield audio chunks
    def audio_generator():
        # Replace with actual audio streaming logic
        yield b'audio_chunk_1'
        yield b'audio_chunk_2'
        # Add more audio chunks as needed

    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator())
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == '__main__':
    stream_with_language()