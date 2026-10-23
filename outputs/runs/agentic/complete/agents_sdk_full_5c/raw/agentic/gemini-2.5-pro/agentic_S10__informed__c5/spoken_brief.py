import os
from elevenlabs import save
from elevenlabs.client import ElevenLabs

def generate_spoken_brief(text: str, output_path: str = "briefing.mp3"):
    """
    Generate a spoken brief from the model output using ElevenLabs.
    """
    try:
        api_key = os.environ["ELEVENLABS_API_KEY"]
        client = ElevenLabs(api_key=api_key)
    except KeyError:
        print("Error: ELEVENLABS_API_KEY environment variable not set.")
        return

    try:
        # Generate audio using a pre-made voice
        audio = client.generate(
            text=text,
            voice="Rachel", # A popular pre-made voice from ElevenLabs
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to a file
        if audio:
            save(audio, output_path)
            print(f"Audio content written to file {output_path}")

    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")
