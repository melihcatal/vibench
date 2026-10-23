import os
from typing import List, Tuple
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def retrieval_audio_brief(
    retrieved_results: List[Tuple[str, float]], output_file: str = "retrieval_brief.mp3"
) -> None:
    brief_text = "Here is a brief of the top retrieval results: " + ". ".join(
        [
            f"Result with similarity {sim:.3f}: {doc[:150]}..."
            for doc, sim in retrieved_results
        ]
    )
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=brief_text, voice="21m00Tcm4TlvDq8ikWAM", model="eleven_monolingual_v1"
    )
    save(audio, output_file)
