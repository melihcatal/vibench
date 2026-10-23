import os
from elevenlabs.client import ElevenLabs

def spoken_brief(text: str, output_path: str):
    """
    Generates a spoken audio brief from text using the ElevenLabs API.

    Saves the audio to the specified output path.
    Requires an ELEVENLABS_API_KEY environment variable.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    # Provider-specific client: elevenlabs.client.ElevenLabs
    client = ElevenLabs(api_key=api_key)

    # Generate audio from text
    # Provider-specific model ID: "eleven_multilingual_v2"
    audio = client.generate(
        text=text,
        voice="Rachel", 
        model="eleven_multilingual_v2"
    )

    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
