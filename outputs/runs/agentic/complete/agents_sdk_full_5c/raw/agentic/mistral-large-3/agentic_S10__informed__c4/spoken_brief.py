import os
from typing import Optional
from elevenlabs import generate, save


def generate_spoken_brief(
    text: str,
    voice: Optional[str] = "Rachel",
    model: Optional[str] = "eleven_multilingual_v2"
) -> str:
    """
    Generate a spoken brief from the model output using ElevenLabs TTS.
    """
    audio = generate(
        text=text,
        voice=voice,
        model=model,
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )
    
    output_path = "spoken_brief.mp3"
    save(audio, output_path)
    
    return output_path