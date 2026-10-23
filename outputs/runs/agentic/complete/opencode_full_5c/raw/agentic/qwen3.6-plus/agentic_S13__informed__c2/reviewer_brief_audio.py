import os

from elevenlabs import ElevenLabs

VOICE_ID = "pNInz6obpgDQGcFmaJgB"
MODEL_ID = "eleven_multilingual_v2"


def generate_reviewer_brief_audio(
    brief_text: str,
    voice_id: str = VOICE_ID,
    model_id: str = MODEL_ID,
) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is required. "
            "Set it to your ElevenLabs API key."
        )

    client = ElevenLabs(api_key=api_key)

    audio_generator = client.text_to_speech.convert(
        text=brief_text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    return audio_bytes
