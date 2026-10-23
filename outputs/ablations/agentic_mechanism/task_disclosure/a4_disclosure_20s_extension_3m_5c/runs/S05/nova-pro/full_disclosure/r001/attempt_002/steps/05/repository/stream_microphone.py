import os
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import types

# Set up the client
client = speech.SpeechClient()

def stream_microphone_audio():
    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    # Stream audio from the microphone
    with open('microphone_audio.raw', 'rb') as audio_file:
        audio_generator = audio_file
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Yield interim transcripts
        for response in responses:
            for result in response.results:
                yield result.alternatives[0].transcript

if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your-service-account-file.json'
    for transcript in stream_microphone_audio():
        print(transcript)