import os
from google.cloud import speech

def stream_microphone():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    print('Start speaking:')

    def callback(response):
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

    with client.streaming_recognize(streaming_config, callback) as stream:
        while True:
            try:
                audio_content = input()
                stream.send_audio(audio_content)
            except KeyboardInterrupt:
                break
    stream.finish()