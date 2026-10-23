import os
from google.cloud import speech_v1 as speech

def get_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    client = speech.SpeechClient()
    return client

class StreamingClient:
    def __init__(self):
        self.client = get_client()

    def start_stream(self, language="en-US", punctuation=True):
        config = {"encoding": "LINEAR16", "sample_rate_hertz": 16000, "language_code": language, "enable_automatic_punctuation": punctuation}
        streaming_config = {"config": config}
        self.stream = self.client.streaming_recognize(streaming_config)
        return self.stream

    def send_audio(self, audio_data):
        self.stream.send(audio_data)

    def receive_transcript(self):
        response = next(self.stream)
        for result in response.results:
            return result.alternatives[0].transcript

    def get_microphone_data(self):
        # Placeholder for microphone data retrieval
        return b"audio data"

    def iter_results(self):
        for response in self.stream:
            for result in response.results:
                yield result