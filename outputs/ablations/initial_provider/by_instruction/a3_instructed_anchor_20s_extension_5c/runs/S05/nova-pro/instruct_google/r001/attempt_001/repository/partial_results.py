import os
from google.cloud import speech

def partial_results():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    def callback(response):
        for result in response.results:
            if not result.is_final:
                print('Partial transcript: {}'.format(result.alternatives[0].transcript))
            else:
                print('Final transcript: {}'.format(result.alternatives[0].transcript))

    with client.streaming_recognize(streaming_config, callback) as stream:
        while True:
            try:
                audio_content = input()
                stream.send_audio(audio_content)
            except KeyboardInterrupt:
                break
    stream.finish()