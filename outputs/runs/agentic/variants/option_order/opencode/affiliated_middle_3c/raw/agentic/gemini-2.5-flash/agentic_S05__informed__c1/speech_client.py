import os
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()


class SpeechClient:
    def __init__(self):
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        if not DEEPGRAM_API_KEY:
            raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
        self.deepgram = Deepgram(DEEPGRAM_API_KEY)

    def get_streaming_recognizer(self, config=None):
        if config is None:
            config = {"smart_format": True, "interim_results": True}
        return self.deepgram.transcription.live(config)
