from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import types

def stream_microphone():
    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    with MicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))

class MicrophoneStream:
    def __init__(self, rate):
        self.rate = rate
        self.stream = None

    def generator(self):
        self.stream = Microphone(sample_rate=self.rate).stream()
        while True:
            yield self.stream.read(4096)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.stream is not None:
            self.stream.stop_recording()

if __name__ == '__main__':
    stream_microphone()