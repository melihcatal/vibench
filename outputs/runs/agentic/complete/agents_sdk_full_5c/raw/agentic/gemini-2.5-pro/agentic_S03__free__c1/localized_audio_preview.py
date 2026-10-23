import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_preview(text: str, output_path: str):
    """
    Generates a spoken audio preview of translated text.
    Provider: ElevenLabs
    
    Requires the ELEVENLABS_API_KEY environment variable.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    # Provider-specific client class from the ElevenLabs SDK
    client = ElevenLabs(api_key=api_key)

    # Generate audio using a provider-specific voice ID and model ID
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    # Save the generated audio to a file
    save(audio, output_path)
    print(f"Audio preview saved to {output_path}")
