from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def generate_platform_brief_audio(output: str) -> str:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio_url = client.text_to_speech(text=output)
    return audio_url
