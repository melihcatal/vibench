import os
from openai import OpenAI
from speech_models import EmbeddingResult

def get_caption_embedding(text: str) -> EmbeddingResult:
    """
    Creates a vector embedding for a caption chunk using OpenAI's API.

    Requires OPENAI_API_KEY environment variable to be set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # Ensure the text is not empty and clean it up
    text = text.strip()
    if not text:
        # OpenAI API errors on empty strings
        return EmbeddingResult(text=text, embedding=[])

    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"  # A specific, identifiable model
    )

    embedding = response.data[0].embedding

    return EmbeddingResult(
        text=text,
        embedding=embedding
    )
