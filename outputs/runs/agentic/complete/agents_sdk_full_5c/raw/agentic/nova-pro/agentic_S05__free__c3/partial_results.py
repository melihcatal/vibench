from google.cloud import speech
from speech_client import create_speech_client

client = create_speech_client()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
)
streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

def handle_partial_results(response):
    for result in response.results:
        if not result.is_final:
            print('Interim: ', result.alternatives[0].transcript)
        else:
            print('Final: ', result.alternatives[0].transcript)