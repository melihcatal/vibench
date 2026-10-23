import os
from google.cloud import speech_v1p1beta1 as speech

def streaming_recognize():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    with open('audio_file.raw', 'rb') as audio_file:
        content = audio_file.read()

        requests = (speech.StreamingRecognizeRequest(audio_content=content[i:i+1024])
                    for i in range(0, len(content), 1024))

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    streaming_recognize()