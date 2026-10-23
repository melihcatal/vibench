# HELPER: speech_client.py
# Local configuration, credential loading, and reusable client utilities for Text-to-Speech

import os
import ibm_watson
from ibm_watson import TextToSpeechV1

# Configuration variables (populate via environment variables)
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

# Create a reusable SDK client on import
_tts_client = None


def get_client() -> TextToSpeechV1:
    """Return a configured Watson Text-to-Speech client.

    Lazily initializes the client using stored credentials.
    """
    global _tts_client
    if _tts_client is None:
        if not IBM_TTS_APIKEY or not IBM_TTS_URL:
            raise RuntimeError(
                "IBM_TTS_APIKEY and IBM_TTS_URL must be set in environment"
            )
        _tts_client = TextToSpeechV1(
            authenticator=ibm_watson.IamAuthenticator(IBM_TTS_APIKEY)
        )
        _tts_client.set_service_url(IBM_TTS_URL)
    return _tts_client


# Example usage
if __name__ == "__main__":
    client = get_client()
    voices = client.list_voices().get_result().get("voices", [])
    print("Available voices count:", len(voices))
