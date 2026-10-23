import os
from google.cloud import speech_v1 as speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Set environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'

def stream_microphone():
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_separate_recognition_per_channel=True,
        model='phone_call'
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    def callback(response):
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

    with open('microphone_stream.raw', 'rb') as audio_file:
        audio_generator = audio_file.read(1024)
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        client.streaming_recognize(streaming_config, requests, callback=callback)

if __name__ == '__main__':
    stream_microphone()