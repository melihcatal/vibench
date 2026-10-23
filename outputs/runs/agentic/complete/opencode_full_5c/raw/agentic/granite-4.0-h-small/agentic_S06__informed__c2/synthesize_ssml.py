# [SAME-SCENARIO] synthesize_ssml.py
# synthesizes SSML with voice and prosody controls using Watson Text to Speech

import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load credentials from environment variables
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")


def synthesize_ssml(ssml: str, voice: str = "en-US-MichaelV3Voice") -> bytes:
    """Synthesize SSML input to an audio byte stream.

    Args:
        ssml (str): The SSML string to synthesize.
        voice (str): The voice identifier.

    Returns:
        bytes: The synthesized audio as binary data.
    """
    authenticator = IAMAuthenticator(IBM_TTS_APIKEY)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(IBM_TTS_URL)
    response = tts.synthesize(ssml, voice=voice, accept="audio/wav")
    if not response.get_result():
        raise RuntimeError(
            f"SSML synthesis failed: {response.get_status_code()} {response.get_message()}"
        )
    # Return raw audio bytes (WAV format)
    return response.get_result().content


# Example usage
if __name__ == "__main__":
    ssml = "<speak><voice name='en-US-MichaelV3Voice'>Hello, this is a <prosody rate='slow'>demonstration</prosody> of SSML synthesis.</voice></speak>"
    audio_bytes = synthesize_ssml(ssml)
    print(f"Synthesized audio size: {len(audio_bytes)} bytes")
