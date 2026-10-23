from google.cloud import speech

class SpeechClient:
    def __init__(self, language_code: str = "en-US", sample_rate_hertz: int = 16000):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            streaming_limit_ms=290000,
            interim_results=True,
            enable_automatic_punctuation=True,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True,
        )

    def get_streaming_config(self):
        return self.streaming_config

    def get_client(self):
        return self.client
