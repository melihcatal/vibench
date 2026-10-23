import os
from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

def stream_with_language():
    config = speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                             sample_rate_hertz=16000,
                                             language_code='en-US',
                                             enable_automatic_punctuation=True)
    streaming_config = speech.types.StreamingRecognitionConfig(config=config)

    with speech.MicrophoneStream() as stream:
        for request in stream:
            response = client.streaming_recognize(streaming_config, request)
            for result in response.results:
                yield result.alternatives[0].transcript

if __name__ == '__main__':
    for transcript in stream_with_language():
        print(transcript)