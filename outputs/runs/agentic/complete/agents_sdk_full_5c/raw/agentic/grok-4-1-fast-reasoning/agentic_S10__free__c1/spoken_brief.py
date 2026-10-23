import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from typing import Optional

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

def generate_spoken_brief(text: str, voice_id: Optional[str] = '21m00Tcm4TlvDq8ikWAM') -> bytes:
    \"\"\"Generate a spoken brief from the model output using ElevenLabs.\"\"
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id='eleven_monolingual_v1',
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
    )
    return audio
