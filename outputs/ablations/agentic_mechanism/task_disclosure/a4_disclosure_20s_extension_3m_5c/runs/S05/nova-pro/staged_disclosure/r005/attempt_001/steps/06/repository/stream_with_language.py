from google.cloud import speech_v1 as speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

def stream_with_language():
    streaming_config = types.StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            enable_automatic_punctuation=True),
        interim_results=False)

    audio_generator = generate_audio()
    requests = (types.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

def generate_audio():
    # Placeholder for audio generation
    yield b'audio_data'