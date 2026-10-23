# SAME-SCENARIO: synthesize_ssml.py
# Synthesize SSML with voice and prosody controls using IBM Watson Text-to-Speech (Watson TTS)

import os
import ibm_watson
from ibm_watson import TextToSpeechV1

# Load credentials from environment variables (ensure they are set before running)
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

# Initialize client using SDK
tts_client = TextToSpeechV1(authenticator=ibm_watson.IamAuthenticator(IBM_TTS_APIKEY))
tts_client.set_service_url(IBM_TTS_URL)


def synthesize_ssml(ssml: str, output_format: str = "audio/flac") -> bytes:
    """Synthesize SSML to audio bytes.

    Args:
        ssml: SSML string with tags such as <voice>, <prosody>, etc.
        output_format: Desired audio format (e.g., 'audio/flac', 'audio/wav').

    Returns:
        Audio data as a byte string.
    """
    with tts_client as client:
        response = client.synthesize_speech(
            ssml=ssml, acceptance=output_format, voice="en-US_MichaelV3Voice"
        )
        # response.get_result() returns streaming body; read bytes
        return response.get_result().read()


# Example usage
if __name__ == "__main__":
    sample_ssml = "<speak><voice name='en-US_MichaelV3Voice'>Hello, <prosody rate='slow'>this is a text-to-speech test with SSML.</prosody></voice></speak>"
    audio_bytes = synthesize_ssml(sample_ssml)
    print("SSML synthesis completed, audio size:", len(audio_bytes), "bytes")
