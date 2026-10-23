from elevenlabs.client import ElevenLabs

VOICE = "Rachel"
MODEL = "eleven_turbo_v2_5"


def reviewer_brief_audio(text: str) -> bytes:
    client = ElevenLabs(api_key=None)
    audio = client.text_to_speech.convert(text=text, voice_id=VOICE, model_id=MODEL)
    return b"".join(audio)
