import os
from speech_client import get_tts_client
from speech_models import normalize_text

def synthesize_text(text: str, voice_id: str = None) -> bytes:
    """Synthesize plain text to an audio byte stream using Azure Speech TTS.

    Args:
        text: The text to synthesize.
        voice_id: Optional voice identifier (e.g., 'en-US-JennyNeural').

    Returns:
        Raw audio bytes (e.g., in ogg/opus format).
    """
    client = get_tts_client()
    # Ensure text is plain (remove SSML tags if present)
    plain_text = normalize_text(text)
    response = client.synthesize_speech(
        speech_config={
            "Language": client.default_language,
            "VoiceName": voice_id,
        },
        audio_config={"Format": "OggOpus"},
        text=plain_text,
    )
    return response.audio_data

if __name__ == "__main__":
    sample = "Hello, world!"
    audio_bytes = synthesize_text(sample, voice_id="en-US-JennyNeural")
    print("Synthesized audio length:", len(audio_bytes))