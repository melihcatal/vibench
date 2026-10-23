import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_spoken_brief(text: str, output_path: str = "briefing.mp3"):
    """
    Generates a spoken audio file from text using the ElevenLabs API.
    
    Requires an ELEVENLABS_API_KEY environment variable.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        
    client = ElevenLabs(api_key=api_key)

    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )
    
    save(audio, output_path)
    print(f"Audio content saved to {output_path}")
