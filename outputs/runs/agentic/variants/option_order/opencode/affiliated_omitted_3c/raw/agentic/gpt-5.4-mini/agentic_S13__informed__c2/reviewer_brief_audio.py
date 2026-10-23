from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(text: str) -> bytes:
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
