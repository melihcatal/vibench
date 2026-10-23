# [LATER-STEP] tts_qa_transcript.py
# Transcribe synthesized QA samples to verify spoken output using Watson Speech to Text

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe an audio byte stream to text.

    Args:
        audio_bytes (bytes): Raw audio data.

    Returns:
        str: Recognized transcript.
    """
    api_key = os.getenv("IBM_STT_APIKEY")
    url = os.getenv("IBM_STT_URL")
    if not api_key or not url:
        raise RuntimeError("IBM_STT_APIKEY or IBM_STT_URL not set")
    authenticator = IAMAuthenticator(api_key)
    client = SpeechToTextV1(authenticator=authenticator, service_url=url)
    with open("temp_qa.wav", "wb") as f:
        f.write(audio_bytes)
    with open("temp_qa.wav", "rb") as audio_file:
        response = client.recognize(
            audio=audio_file, content_type="audio/lwav"
        ).get_result()
    transcript = (
        response.get("results", [{}])[0]
        .get("alternatives", [{}])[0]
        .get("transcript", "")
    )
    return transcript
