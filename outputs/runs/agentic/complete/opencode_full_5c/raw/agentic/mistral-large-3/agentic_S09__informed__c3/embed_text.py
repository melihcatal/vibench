import os
import numpy as np
from openai import OpenAI
from typing import List, Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generate an embedding vector for a single text string using OpenAI Embeddings."""
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
