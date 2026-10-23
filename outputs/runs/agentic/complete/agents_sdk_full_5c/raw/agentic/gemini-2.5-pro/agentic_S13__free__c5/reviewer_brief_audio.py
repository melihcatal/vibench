from safety_client import get_elevenlabs_client
from safety_models import AudioBriefRequest

def reviewer_brief_audio(request: AudioBriefRequest):
    """
    Generates a spoken audio brief for a moderation reviewer using ElevenLabs API.

    Args:
        request: An AudioBriefRequest with the text and output file path.
    """
    client = get_elevenlabs_client()
    
    # Generate the audio from the input text
    # Using a professional-sounding voice like "Adam"
    audio = client.generate(
        text=request.text,
        voice="Adam",
        model="eleven_multilingual_v2"
    )

    # Save the generated audio to the specified file
    with open(request.output_path, 'wb') as f:
        f.write(audio)
        
    print(f"Audio brief saved to {request.output_path}")
