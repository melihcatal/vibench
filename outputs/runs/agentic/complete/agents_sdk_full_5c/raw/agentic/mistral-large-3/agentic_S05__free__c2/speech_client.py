from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import os

def get_speech_client():
    client = SpeechClient()
    return client

def streaming_recognize(client, config, callback):
    request = cloud_speech.StreamingRecognizeRequest(**config)
    return client.streaming_recognize(requests=[request], callback=callback)