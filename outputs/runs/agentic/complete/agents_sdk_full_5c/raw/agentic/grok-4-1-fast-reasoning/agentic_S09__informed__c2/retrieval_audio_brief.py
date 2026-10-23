import os
from typing import List
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings

def retrieval_audio_brief(retrieved_results: List[str]) -> bytes:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError('ELEVENLABS_API_KEY environment variable is required.')
    client = ElevenLabs(api_key=api_key)
    brief_text = 'Top retrieval results: ' + '; '.join(retrieved_results[:5])
    audio = client.generate(
        text=brief_text,
        voice=Voice(
            voice_id='21m00Tcm4TlvDq8ikWAM',
            model_id='eleven_monolingual_v1'
        ),
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75
        )
    )
    return audio
