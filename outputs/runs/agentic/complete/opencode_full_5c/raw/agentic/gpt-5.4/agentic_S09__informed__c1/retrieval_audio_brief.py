import os

from elevenlabs import ElevenLabs


def generate_audio_brief(
    results: list[dict],
    *,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    summary_text = " ".join(str(item.get("text", "")) for item in results[:3]).strip()
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=summary_text,
    )
    if isinstance(audio, bytes):
        return audio
    return b"".join(chunk for chunk in audio)
