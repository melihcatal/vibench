import os
from elevenlabs import generate, set_api_key

def generate_audio_brief(text: str, voice_id: str = None) -> bytes:
    """Generates a spoken audio brief from retrieved search results using Eleven Labs Text-to-Speech API.
    Returns the audio content as bytes."""
    
    elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    set_api_key(elevenlabs_api_key)

    if voice_id is None:
        # Use a default voice if not provided
        # Example voice IDs: '21m00Tcm4obsnbMyryWj' (Rachel), 'pNInz6obpgDQGcFmaJgB' (Adam)
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4obsnbMyryWj") 

    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2" 
    )
    
    return audio