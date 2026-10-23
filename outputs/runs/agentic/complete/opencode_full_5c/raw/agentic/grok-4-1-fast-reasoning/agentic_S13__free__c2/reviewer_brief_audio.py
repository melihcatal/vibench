from safety_client import get_elevenlabs_client
from typing import Optional


def reviewer_brief_audio(
    brief: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    output_path: Optional[str] = None,
) -> bytes:
    client = get_elevenlabs_client()
    if client is None:
        raise ValueError("ElevenLabs API key not configured")
    audio = client.generate(
        text=brief,
        voice=voice_id,
        model="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio)
    return audio
