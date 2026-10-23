import os
from elevenlabs import ElevenLabs

# Initialize ElevenLabs client using environment variable
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def synthesize_plain_text(
    text: str, voice_id: str = "11ead5fc-4bcf-4e4e-8c38-49d03cefae29"
) -> bytes:
    """Synthesize plain text to an audio byte stream using ElevenLabs TTS.

    Args:
        text (str): The input plain text to synthesize.
        voice_id (str): The ElevenLabs voice identifier. Defaults to default voice.

    Returns:
        bytes: The synthesized audio as a raw byte stream.
    """
    response = client.text_to_speech(text, voice_id=voice_id)
    return response.audio_content
