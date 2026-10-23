import os
from elevenlabs import Client, Voice, VoiceSettings, Audio


def synthesize_ssml(ssml: str) -> Audio:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = Client(api_key=api_key)
    voice = Voice(voice_id="your_voice_id")
    audio = client.text_to_speech(text=ssml, voice=voice)
    return audio
