from elevenlabs import ElevenLabs


def reviewer_brief_audio(text: str) -> bytes:
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        text=text, voice_id="Rachel", model_id="eleven_multilingual_v2"
    )
    return b"".join(audio)
