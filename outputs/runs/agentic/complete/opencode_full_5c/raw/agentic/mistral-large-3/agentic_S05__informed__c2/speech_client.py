import os
from typing import Optional
from deepgram import Deepgram

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


class SpeechClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or DEEPGRAM_API_KEY
        self.client = Deepgram(self.api_key)

    async def get_live_connection(self, options: dict):
        return await self.client.transcription.live(options)

    def validate_options(self, options: dict) -> bool:
        required_keys = ["language", "punctuate", "interim_results"]
        return all(key in options for key in required_keys)
