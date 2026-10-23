import os
from elevenlabs.client import ElevenLabs
from model_models import AudioBriefResult


def platform_brief_audio(text: str) -> AudioBriefResult:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
    )
    audio_bytes = b"".join(audio)
    return AudioBriefResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        raw_response=audio,
    )
