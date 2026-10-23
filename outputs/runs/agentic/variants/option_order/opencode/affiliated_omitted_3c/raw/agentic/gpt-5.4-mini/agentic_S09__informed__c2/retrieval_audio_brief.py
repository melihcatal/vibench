import os

from elevenlabs import ElevenLabs


def retrieval_audio_brief(summary_text: str) -> bytes:
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
    audio = client.text_to_speech.convert(
        text=summary_text,
        voice_id=os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
    )
    return b"".join(audio)
