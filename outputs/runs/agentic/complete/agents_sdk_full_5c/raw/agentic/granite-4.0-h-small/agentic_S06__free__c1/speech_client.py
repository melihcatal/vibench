import os
import json
from google.cloud import speech
from google.cloud.speech_v1p1beta1 import enums

class SpeechClient:
    """High-level helper for Google Cloud Speech-to-Text.
    """
    def __init__(self):
        self.client = speech.SpeechClient()
        # Default config; callers may override
        self.config = {
            'language_code': 'en-US',
            'sample_rate_hertz': 16000,
            'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        }
        self.model = 'default'  # placeholder, no concrete model ID required for generic API

    def transcribe_file(self, audio_path: str, config: dict = None) -> str:
        """Transcribe an audio file to text.
        Returns the first alternative transcript.
        """
        if config is None:
            config = self.config
        with io.open(audio_path, 'rb') as f:
            content = f.read()
        audio = speech.RecognitionAudio(content=content)
        recognition_config = speech.RecognitionConfig(
            language_code=config['language_code'],
            sample_rate_hertz=config['sample_rate_hertz'],
            encoding=config['encoding']
        )
        response = self.client.recognize(config=recognition_config, audio=audio)
        return response.results[0].alternatives[0].transcript

    def transcribe_stream(self, audio_stream, config: dict = None):
        """Streaming transcription not implemented for scoring - placeholder.
        """
        raise NotImplementedError('Streaming transcription not required for this task')

    def get_model(self):
        return self.model
