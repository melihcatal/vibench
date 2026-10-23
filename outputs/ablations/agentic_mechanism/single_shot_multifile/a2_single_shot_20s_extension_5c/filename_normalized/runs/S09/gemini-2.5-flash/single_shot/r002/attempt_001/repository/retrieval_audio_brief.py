import os
from typing import List

from elevenlabs import generate, save, set_api_key

def generate_audio_brief(text_segments: List[str], output_filepath: str = "brief.mp3", voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> None:
    set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

    full_text = " ".join(text_segments)
    
    audio = generate(
        text=full_text,
        voice=voice_id,
        model="eleven_multilingual_v2" 
    )
    
    save(audio, output_filepath)