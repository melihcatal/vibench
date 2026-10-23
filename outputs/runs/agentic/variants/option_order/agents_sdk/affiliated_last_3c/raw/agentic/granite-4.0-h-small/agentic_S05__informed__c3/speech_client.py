# [HELPER] speech_client.py
import os
from typing import Any, Dict

# Conrete provider: Google Cloud Speech-to-Text
# Provides a thin wrapper around google-cloud-speech client for streaming scenarios

from google.cloud import speech_v1p1beta1 as speech

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError('Set GOOGLE_APPLICATION_CREDENTIALS environment variable')


class SpeechClient:
    def __init__(self):
        self.client = speech.SpeechClient()

    def create_config(self,
                      language_code: str = 'en-US',
                      enable_automatic_punctuation: bool = True,
                      sample_rate_hertz: int = 16000,
                      model: str = 'default') -> speech.types.RecognitionConfig:
        """
        Build a Google Speech recognition config with optional parameters.
        model can be 'default', 'phone_call', 'video', etc.","""
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
            model=model,
        )

    def create_request(self, audio_source: Any, config: speech.types.RecognitionConfig,
                       interim_results: bool = False) -> Dict[str, Any]:
        """
        Build a streaming request payload.","""
        return {
            'config': config,
            'audio_source': audio_source,
            'single_utterance': False,
            'interim_results': interim_results,
        }

    # Example of how you could start a streaming call using the generated request.
    # Integration code would then feed audio to the returned stub._streaming_stub.
    # For this helper we just expose creation utilities so higher-level same-scenario files can focus on flow.

if __name__ == '__main__':
    client = SpeechClient()
    config = client.create_config(language_code='es-ES', enable_automatic_punctuation=True)
    request = client.create_request(None, config)
    print('Config example:', config)
    print('Request example:', request)
