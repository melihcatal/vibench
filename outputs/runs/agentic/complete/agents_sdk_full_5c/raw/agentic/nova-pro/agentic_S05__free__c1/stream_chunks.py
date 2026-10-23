import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

config = {
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
    'sample_rate_hertz': 16000,
    'language_code': 'en-US',
}
streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

def stream_chunks(audio_chunks):
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                 for chunk in audio_chunks)
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            print(result.alternatives[0].transcript)