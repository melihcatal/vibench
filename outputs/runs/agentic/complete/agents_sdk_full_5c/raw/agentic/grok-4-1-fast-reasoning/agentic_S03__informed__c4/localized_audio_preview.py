import os
from elevenlabs import generate

def generate_localized_audio_preview(text: str, output_path: str) -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    
    # Multilingual voice and model
    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella (multilingual)
    model_id = "eleven_multilingual_v2"
    
    audio = generate(
        text=text,
        voice=voice_id,
        model=model_id,
        api_key=api_key,
        output_format="mp3_22050_32"
    )
    
    with open(output_path, "wb") as file:
        file.write(audio)
