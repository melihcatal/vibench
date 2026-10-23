from google.cloud import speech
from speech_models import StreamingRecognitionConfig

class SpeechClient:
    def __init__(self):
        self.client = speech.SpeechClient()

    def get_streaming_config(self, config: StreamingRecognitionConfig):
        return speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding[config.encoding],
                sample_rate_hertz=config.sample_rate_hertz,
                language_code=config.language_code,
                enable_automatic_punctuation=config.enable_automatic_punctuation,
            ),
            interim_results=config.interim_results,
        )
