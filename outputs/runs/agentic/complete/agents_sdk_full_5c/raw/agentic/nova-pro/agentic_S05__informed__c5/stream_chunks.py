import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def stream_chunks():
    with open('audio.wav', 'rb') as f:
        audio_content = f.read()
    config = speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                            sample_rate_hertz=16000,
                                            language_code='en-US')
    streaming_config = speech.types.StreamingRecognitionConfig(config=config)

    requests = [speech.types.StreamingRecognizeRequest(audio_content=audio_content)]
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            yield result.alternatives[0].transcript