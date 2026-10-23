import os
from typing import List, Dict, Any

from elevenlabs import generate, set_api_key


def generate_audio_brief(search_results: List[Dict[str, Any]], output_file: str) -> None:
    """Generate a spoken brief from retrieved search results using ElevenLabs."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    
    set_api_key(api_key)
    
    brief_text = "Here are the top search results:\n"
    for idx, result in enumerate(search_results, 1):
        brief_text += f"Result {idx}: {result.get('text', 'No text available')}\n"
    
    audio = generate(text=brief_text, voice="Rachel", model="eleven_multilingual_v2")
    with open(output_file, "wb") as f:
        f.write(audio)