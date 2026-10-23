# [SAME-SCENARIO] synthesize_text.py
# synthesizes plain text to an audio byte stream using Azure Speech TTS

import os
from azure.cognitiveservices.speech import (
    SpeechConfig,
    AudioDataStream,
    SpeechSynthesizer,
)

# Load credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def synthesize_text(plain_text: str, voice_name: str = "en-US-JennyNeural") -> bytes:
    """Synthesize plain text to an audio byte stream.

    Args:
        plain_text (str): The text to synthesize.
        voice_name (str): The voice to use.

    Returns:
        bytes: The synthesized audio as a byte stream.
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    speech_config.speech_synthesis_voice_name = voice_name
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    # Synthesize to an in‑memory audio stream
    result = synthesizer.speak_text_async(plain_text).get()
    if result.reason != result.reason.Success:
        raise RuntimeError(f"Synthesis failed: {result.reason}")
    audio_stream = AudioDataStream(result)
    # Return raw PCM bytes (16‑bit little‑endian, 1 channel)
    return audio_stream.get_audio()


# Example usage
if __name__ == "__main__":
    text = "Hello, welcome to the text‑to‑speech demo."
    audio_bytes = synthesize_text(text)
    print("Synthesized audio size:", len(audio_bytes))
