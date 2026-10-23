import os
from embeddings_client import get_elevenlabs_client

def generate_audio_brief(text_brief: str, output_dir: str = "/tmp") -> str:
    """
    Generates a spoken audio brief from retrieved search results text
    using the ElevenLabs Text-to-Speech API.

    Args:
        text_brief: The text to convert to speech.
        output_dir: The directory to save the audio file.

    Returns:
        The file path of the generated audio file.
    """
    elevenlabs_client = get_elevenlabs_client()

    audio_stream = elevenlabs_client.generate(
        text=text_brief,
        voice="Rachel",  # A specific voice model
        model="eleven_multilingual_v2"  # A specific TTS model
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "retrieval_brief.mp3")
    
    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
            
    return output_path
