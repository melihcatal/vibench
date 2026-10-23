import os
from typing import List, Dict
from elevenlabs import generate, set_api_key


def generate_audio_brief(search_results: List[Dict[str, str]]) -> bytes:
    """Generate a spoken brief from retrieved search results using ElevenLabs TTS."""
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    
    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(search_results, 1):
        brief_text += f"Result {idx}: {result.get('content', '')}\n"
    
    audio = generate(text=brief_text, voice="Rachel", model="eleven_multilingual_v2")
    return audio