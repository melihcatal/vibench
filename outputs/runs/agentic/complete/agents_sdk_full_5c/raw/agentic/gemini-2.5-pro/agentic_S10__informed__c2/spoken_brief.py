import os
from elevenlabs.client import ElevenLabs

def generate_spoken_brief(text: str, output_path: str) -> bool:
    """
    Generates a spoken brief from text using the ElevenLabs API and saves it to a file.

    Requires the ELEVENLABS_API_KEY environment variable.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        client = ElevenLabs(api_key=api_key)
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )

        with open(output_path, "wb") as f:
            f.write(audio)
        
        return True
        
    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")
        return False
