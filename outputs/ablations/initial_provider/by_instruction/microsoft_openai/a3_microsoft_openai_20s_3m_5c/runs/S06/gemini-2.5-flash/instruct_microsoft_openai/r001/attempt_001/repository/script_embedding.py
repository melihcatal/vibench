import cohere
import os
from typing import List

def script_embedding(text: str) -> List[float]:
    """
    Embeds narration scripts for voice-asset search using Cohere.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = co.embed(
        texts=[text],
        model="embed-english-v3.0"
    )

    return response.embeddings[0]
