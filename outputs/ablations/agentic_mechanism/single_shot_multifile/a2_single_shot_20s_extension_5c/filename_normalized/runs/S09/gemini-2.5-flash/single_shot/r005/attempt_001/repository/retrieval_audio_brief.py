import os
from typing import List
from elevenlabs import generate, save, set_api_key

def generate_audio_brief(text_summary: str, output_filepath: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    set_api_key(api_key)
    
    audio = generate(
        text=text_summary,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    
    save(audio, output_filepath)
