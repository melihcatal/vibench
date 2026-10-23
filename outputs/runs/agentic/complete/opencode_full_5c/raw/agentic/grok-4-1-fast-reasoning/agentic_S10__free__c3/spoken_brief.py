from model_client import get_elevenlabs_client


def generate_spoken_brief(text: str) -> bytes:
    client = get_elevenlabs_client()
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_turbo_v2",
        output_format="mp3_44100_128",
    )
    return audio
