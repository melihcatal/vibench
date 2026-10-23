import os
from typing import List, Dict, Any
from elevenlabs import generate, voices


def generate_audio_brief(retrieved_results: List[Dict[str, Any]], voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> bytes:
    """
    Generate a spoken brief from retrieved search results using ElevenLabs TTS.
    
    Args:
        retrieved_results: List of retrieved documents with metadata.
        voice_id: ElevenLabs voice ID.
    
    Returns:
        Audio data as bytes.
    """
    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(retrieved_results[:3]):  # Limit to top 3
        brief_text += f"Result {idx + 1}: {result.get('text', '')[:150]}...\n"

    audio = generate(text=brief_text, voice=voice_id, api_key=os.getenv("ELEVENLABS_API_KEY"))
    return audio