import os
from typing import List, Dict, Any


def generate_spoken_brief(text: str, output_file: str = "brief.mp3") -> Dict[str, Any]:
    """
    Generate a spoken brief from text using ElevenLabs Text-to-Speech.
    Requires ELEVENLABS_API_KEY environment variable.
    """
    from elevenlabs import generate, save, set_api_key

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    set_api_key(api_key)

    audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    save(audio, output_file)

    return {"input_text": text, "output_file": output_file, "status": "success"}


def retrieval_audio_brief(
    retrieved_results: List[Dict[str, Any]], output_file: str = "retrieval_brief.mp3"
) -> Dict[str, Any]:
    """
    Generate a spoken brief from retrieved search results using ElevenLabs Text-to-Speech.
    """
    brief_text = "Retrieved results summary:\n"
    for i, result in enumerate(retrieved_results, 1):
        brief_text += f"Result {i}: {result.get('text', 'No text content')}\n"
        if i >= 3:  # Limit to top 3 results for brevity
            break

    return generate_spoken_brief(brief_text, output_file)
