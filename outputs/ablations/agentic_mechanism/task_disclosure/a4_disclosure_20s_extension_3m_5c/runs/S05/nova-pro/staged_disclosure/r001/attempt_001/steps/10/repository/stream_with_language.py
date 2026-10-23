import os
from google.cloud import speech_v1p1beta1 as speech

def stream_with_language():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()
    config = {"encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
               "sample_rate_hertz": 16000,
               "language_code": 'en-US',
               "enable_automatic_punctuation": True}
    streaming_config = {"config": config}

    requests = ({"streaming_config": streaming_config},
                 {"audio_content": b'\x00' * 1024})

    responses = client.streaming_recognize(requests)

    for response in responses:
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    stream_with_language()