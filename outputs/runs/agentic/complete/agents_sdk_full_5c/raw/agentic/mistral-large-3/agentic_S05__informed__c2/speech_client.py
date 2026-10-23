import os
from deepgram import Deepgram

_DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def get_deepgram_client():
    if not _DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return Deepgram(_DEEPGRAM_API_KEY)