import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_spoken_brief(text: str, output_path: str):
    """
    Generates a spoken brief from text using ElevenLabs API and saves it to a file.
    
    Args:
        text (str): The text to be converted to speech.
        output_path (str): The path to save the generated MP3 file.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    client = ElevenLabs(api_key=api_key)

    try:
        # Generate audio from the text
        audio = client.generate(
            text=text,
            voice="Rachel",  # A popular, standard voice
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to the specified file path
        save(audio, output_path)
        print(f"Audio content saved to {output_path}")

    except Exception as e:
        print(f"An error occurred while generating speech: {e}")

