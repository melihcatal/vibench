import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types


class SpeechClient:
    """Provides a configured Google Cloud Speech-to-Text client."""

    def __init__(self):
        self.client = speech.SpeechClient()

    def get_client(self):
        return self.client


def get_speech_client():
    """Returns a configured Google Cloud Speech-to-Text client."""
    return SpeechClient().get_client()
