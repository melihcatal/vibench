import os

from elevenlabs import ElevenLabs

from model_models import SpeechResult, normalize_text


def generate_spoken_brief(
    text: str, voice_id: str | None = None, model_id: str = "eleven_multilingual_v2"
) -> dict:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    selected_voice = voice_id or os.getenv(
        "ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"
    )
    audio = client.text_to_speech.convert(
        voice_id=selected_voice,
        model_id=model_id,
        text=normalize_text(text),
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    result = SpeechResult(
        provider="ElevenLabs",
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        voice=selected_voice,
    )
    return {
        "provider": result.provider,
        "voice": result.voice,
        "content_type": result.content_type,
        "audio_bytes": result.audio_bytes,
    }
