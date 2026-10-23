# SAME-SCENARIO: synthesize_text.py
# Synthesize plain text to an audio byte stream using IBM Watson Text-to-Speech (Watson TTS)

import os
import ibm_watson
from ibm_watson import TextToSpeechV1

# Load credentials from environment variables (ensure they are set before running)
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

# Initialize client using SDK
tts_client = TextToSpeechV1(authenticator=ibm_watson.IamAuthenticator(IBM_TTS_APIKEY))
tts_client.set_service_url(IBM_TTS_URL)


def synthesize(text: str, output_format: str = "audio/flac") -> bytes:
    """Synthesize plain text to audio bytes.

    Args:
        text: Plain text to synthesize.
        output_format: Desired audio format (e.g., 'audio/flac', 'audio/wav').

    Returns:
        Audio data as a byte string.
    """
    with tts_client as client:
        response = client.synthesize_speech(
            text=text, voice="en-US_MichaelV3Voice", accept=output_format
        )
        # response.get_result() returns streaming body; read bytes
        return response.get_result().read()


# Example usage
if __name__ == "__main__":
    sample_text = "Hello, this is a test of text to speech."
    audio_bytes = synthesize(sample_text)
    print("Synthesis completed, audio size:", len(audio_bytes), "bytes")
