# [LATER-STEP] tts_qa_transcript.py
# Transcribes synthesized QA samples to verify spoken output.

import os
import json
from typing import Dict, Any


def transcribe_audio(
    audio_bytes: bytes, model_id: str = "en-US_NarrowbandModel"
) -> Dict[str, Any]:
    """Transcribe raw audio to text using IBM Watson Speech to Text.

    Args:
        audio_bytes (bytes): Raw PCM audio data.
        model_id (str): Watson model identifier.

    Returns:
        Dict[str, Any]: Transcription result metadata.
    """
    # ---------------------------------------------------
    # Provider: IBM Watson Speech to Text (SDK)
    # ---------------------------------------------------
    from ibm_watson import SpeechToTextV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    API_KEY = os.getenv("STT_API_KEY")
    SERVICE_URL = os.getenv("STT_URL")
    if not all([API_KEY, SERVICE_URL]):
        raise RuntimeError("STT_API_KEY and STT_URL must be set")
    authenticator = IAMAuthenticator(API_KEY)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(SERVICE_URL)
    with open("temp_audio.raw", "wb") as f:
        f.write(audio_bytes)
    with open("temp_audio.raw", "rb") as audio:
        result = service.recognize(
            audio=audio, content_type="audio/raw", model=model_id
        ).get_result()
    # Clean up temporary file (optional)
    os.remove("temp_audio.raw")
    return {
        "transcription": result.get("results", [{}])[0]
        .get("alternatives", [{}])[0]
        .get("transcript", ""),
        "metadata": result,
    }


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # Assume raw_bytes comes from any TTS synthesis function
#     raw_bytes = b"\x00" * 1024
#     res = transcribe_audio(raw_bytes)
#     print('Transcribed text:', res['transcription'])
