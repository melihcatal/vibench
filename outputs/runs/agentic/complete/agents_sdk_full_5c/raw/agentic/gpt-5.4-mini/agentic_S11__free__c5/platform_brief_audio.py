from model_client import create_platform_client


# Provider-identifying signal: OpenAI text-to-speech with model tts-1.
def generate_spoken_briefing(output_text: str, voice: str = "alloy") -> bytes:
    client = create_platform_client()
    audio = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=output_text,
    )
    return audio.read()
