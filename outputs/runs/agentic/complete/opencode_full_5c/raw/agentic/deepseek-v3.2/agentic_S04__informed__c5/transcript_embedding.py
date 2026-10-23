import os
import openai
from typing import List
from speech_models import split_into_segments


def transcript_embedding(
    transcript_text: str, model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Embed transcript segments for semantic retrieval using OpenAI Embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    segments = split_into_segments(transcript_text, max_segment_length=8000)

    embeddings = []
    for segment in segments:
        response = client.embeddings.create(model=model, input=segment)

        embeddings.append(
            {"text": segment, "embedding": response.data[0].embedding, "model": model}
        )

    return embeddings
