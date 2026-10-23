from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

def start_streaming_recognizer(language_code, enable_automatic_punctuation):
    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )

    streaming_config = types.StreamingRecognitionConfig(config=config)

    # Simulate streaming audio data
    audio_generator = generate_audio_data()

    requests = (types.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print("Transcript: ", result.alternatives[0].transcript)

def generate_audio_data():
    # Placeholder for actual audio data generation
    yield b'This is a test audio data'

if __name__ == '__main__':
    start_streaming_recognizer('en-US', True)