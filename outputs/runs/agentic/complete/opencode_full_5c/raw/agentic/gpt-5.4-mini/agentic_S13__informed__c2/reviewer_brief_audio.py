from elevenlabs import ElevenLabs


client = ElevenLabs()


def reviewer_brief_audio(text: str) -> bytes:
    audio = client.text_to_speech.convert(
        model_id="eleven_multilingual_v2", voice_id="Rachel", text=text
    )
    return b"".join(chunk for chunk in audio)
