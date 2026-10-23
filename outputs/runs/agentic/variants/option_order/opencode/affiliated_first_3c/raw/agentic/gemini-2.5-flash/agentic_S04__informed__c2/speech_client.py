import os
from assemblyai import Client


class SpeechClient:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
        self.client = Client(self.api_key)
