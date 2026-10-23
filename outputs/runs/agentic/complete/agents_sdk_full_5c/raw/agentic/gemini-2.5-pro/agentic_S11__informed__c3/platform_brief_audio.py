import os
from elevenlabs.client import ElevenLabs
from model_models import AudioGenerationRequest

def generate_audio_briefing(request: AudioGenerationRequest, output_path: str):
    """
    Generates an audio file from text using the ElevenLabs API and saves it.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        audio = client.generate(
            text=request.text,
            voice=request.voice_id,
            model=request.model_id
        )

        with open(output_path, "wb") as f:
            f.write(audio)
        
        print(f"Audio content has been saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"Error generating audio with ElevenLabs: {e}")
        raise

if __name__ == '__main__':
    # This part is for demonstration if run directly
    req = AudioGenerationRequest(
        text="This is a test of the text-to-speech system from ElevenLabs."
    )
    output_file = "briefing_audio.mp3"
    generate_audio_briefing(req, output_file)
