import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_briefing_elevenlabs(text: str, output_path: str):
    """
    Generates an audio file from text using the ElevenLabs API.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    client = ElevenLabs(api_key=api_key)
    
    try:
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        
        save(audio, output_path)
        print(f"Audio saved to {output_path}")
    except Exception as e:
        print(f"Error generating audio with ElevenLabs: {e}")
