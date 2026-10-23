import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

def generate_spoken_brief(text: str) -> bytes:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError('ELEVENLABS_API_KEY environment variable is required.')
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.generate(
        model_id='eleven_monolingual_v1',
        text=text,
        voice_id='21m00Tcm4TlvDq8ikWAM',
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
    )
    return audio
