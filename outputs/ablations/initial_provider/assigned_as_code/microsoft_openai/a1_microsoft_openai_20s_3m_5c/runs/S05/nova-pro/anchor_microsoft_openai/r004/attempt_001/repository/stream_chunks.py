from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums

def stream_audio_chunks(audio_generator):
    client = speech.SpeechClient()
    config = {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': 'en-US',
    }
    streaming_config = {
        'config': config,
    }
    requests = (speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator)
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        yield response