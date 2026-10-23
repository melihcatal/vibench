import os
from typing import List
from openai import OpenAI


def embed_moderation_rationale(rationale_text: str) -> List[float]:
    """
    Embeds moderation rationales for case retrieval using OpenAI Embeddings.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model="text-embedding-ada-002",  # A common and capable embedding model
        input=rationale_text,
    )

    return response.data[0].embedding
