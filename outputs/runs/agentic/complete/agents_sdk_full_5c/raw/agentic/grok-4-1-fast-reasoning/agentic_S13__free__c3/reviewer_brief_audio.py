import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from typing import Optional

def reviewer_brief_audio(
    brief_text: str,
    output_path: str = 'reviewer_brief.mp3',
    voice: str = '21m00Tcm4TlvDq8ikWAM',  # Rachel
) -> str:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError('ELEVENLABS_API_KEY environment variable is required.')
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=brief_text,
        voice=voice,
        model='eleven_monolingual_v1',
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
        ),
    )
    with open(output_path, 'wb') as f:
        f.write(audio)
    return output_path
