import os
from elevenlabs import ElevenLabs


def generate_spoken_brief(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2",
) -> bytes:
    api_key = os.environ["ELEVENLABS_API_KEY"]
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice,
        model=model,
    )
    return audio


def generate_spoken_brief_to_file(
    text: str,
    output_path: str,
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2",
) -> str:
    audio_bytes = generate_spoken_brief(text, voice=voice, model=model)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def list_available_voices() -> list[dict]:
    api_key = os.environ["ELEVENLABS_API_KEY"]
    client = ElevenLabs(api_key=api_key)
    voices_response = client.voices.get_all()
    return [
        {
            "voice_id": v.voice_id,
            "name": v.name,
            "category": v.category,
        }
        for v in voices_response.voices
    ]
