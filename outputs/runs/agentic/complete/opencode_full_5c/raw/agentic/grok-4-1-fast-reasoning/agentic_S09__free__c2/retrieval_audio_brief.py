import os
import tempfile
from typing import List, Tuple, Optional
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieval_audio_brief(
    retrieved_results: List[Tuple[str, float]], output_path: Optional[str] = None
) -> str:
    brief_parts = [
        f"Result {i + 1}: {doc[:100]}... score {score:.3f}"
        for i, (doc, score) in enumerate(retrieved_results[:3])
    ]
    brief_text = "Retrieved documents: " + ". ".join(brief_parts) + "."
    if output_path is None:
        output_path = tempfile.mktemp(suffix=".mp3")
    speech_response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )
    speech_response.stream_to_file(output_path)
    return output_path
