import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def handle_partial_results(response):
    for result in response.results:
        if not result.is_final:
            print('Interim: ', result.alternatives[0].transcript)
        else:
            print('Final: ', result.alternatives[0].transcript)