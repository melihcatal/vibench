import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def stream_microphone():
    with speech.MicrophoneStream() as stream:
        for request in stream:
            response = client.streaming_recognize(request)
            for result in response.results:
                yield result.alternatives[0].transcript

if __name__ == '__main__':
    for transcript in stream_microphone():
        print(transcript)