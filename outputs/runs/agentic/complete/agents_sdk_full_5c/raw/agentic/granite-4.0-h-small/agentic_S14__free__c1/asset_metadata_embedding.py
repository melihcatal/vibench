import os
from typing import Tuple, Dict

# Concrete embedding provider: OpenAI embeddings (hosted API)
import openai
from openai.error import OpenAIError

# Simple vector store using ANN (e.g., Chroma, Pinecone) could be added later
# For now we return the raw embedding vector

def embed_metadata_and_text(metadata: Dict[str, str], text: str) -> Tuple[str, list[float]]:
    """Create a content embedding using OpenAI's embedding model.",
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise RuntimeError('OPENAI_API_KEY environment variable not set')

    try:
        response = openai.Embedding.create(
            model='text-embedding-3-large',
            input=f\"{metadata}\\n\\n{text}\"  # concatenate metadata JSON string with text
        )
        embedding = response.data[0].embedding  # list[float]
        return str(metadata), embedding
    except OpenAIError as e:
        raise RuntimeError(f"Embedding error: {e}")
