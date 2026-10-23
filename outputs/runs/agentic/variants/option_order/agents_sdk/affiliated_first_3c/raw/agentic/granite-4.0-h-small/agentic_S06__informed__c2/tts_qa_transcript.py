import os
import re
import pathlib
from typing import List

# Watson Speech to Text SDK import (concrete provider signal)
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Environment variables for authentication
IBM_STT_APIKEY = os.getenv("IBM_STT_APIKEY")
IBM_STT_URL = os.getenv("IBM_STT_URL", "https://api.us-south.speech-to-text.watson.cloud.ibm.com")

if not IBM_STT_APIKEY:
    raise RuntimeError("Set IBM_STT_APIKEY environment variable")

stt_client = SpeechToTextV1(
    authenticator=IAMAuthenticator(IBM_STT_APIKEY),
    service_url=IBM_STT_URL,
)

def transcribe_audio(audio_bytes: bytes) -> List[dict]:
    """Transcribe raw audio bytes (e.g., ogg/opus) to QA transcript.

    Args:
        audio_bytes: Raw audio data produced by synthesis.

    Returns:
        List of recognition results; each entry contains 'alternatives' with text.
    """
    with pathlib.Path("/tmp/tts_qa_audio.ogg").open("wb") as fout:
        fout.write(audio_bytes)
    with open("/tmp/tts_qa_audio.ogg", "rb") as f:
        # Use broadband model for better quality
        response = stt_client.recognize(
            audio=f,
            content_type="audio/ogg",
            model="broadband_model",
        ).get_result()
    return response.get("results", [])

if __name__ == "__main__":
    # Placeholder: assume we have a synthesized audio file path
    sample_path = "/tmp/sample_synthesized.ogg"
    # For demo, just call the function (file must exist)
    try:
        trans = transcribe_audio(open(sample_path, "rb").read())
        print("Transcription results:", trans)
    except FileNotFoundError:
        print("Demo audio file not found. Provide a valid synthesized audio file.")
