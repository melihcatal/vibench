# SAME-SCENARIO: save_audio.py
# Write synthesized speech audio to a local file using IBM Watson TTS

import os
from pathlib import Path
import ibm_watson
from ibm_watson import TextToSpeechV1

# Load credentials from environment variables (ensure they are set before running)
IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")

# Initialize client using SDK
tts_client = TextToSpeechV1(authenticator=ibm_watson.IamAuthenticator(IBM_TTS_APIKEY))
tts_client.set_service_url(IBM_TTS_URL)


def save_audio_file(audio_bytes: bytes, output_path: str) -> None:
    """Save raw audio bytes to a local file.

    Args:
        audio_bytes: Audio data as bytes.
        output_path: Destination file path (e.g., 'output.flac').
    """
    Path(output_path).write_bytes(audio_bytes)
    print(f"Audio saved to {output_path}")


# Example usage (same as previous examples)
if __name__ == "__main__":
    sample_text = "Hello world, this is saved audio."
    audio = synthesize(
        sample_text
    )  # Requires synthesize function from synthesize_text.py
    save_audio_file(audio, "sample_output.flac")
