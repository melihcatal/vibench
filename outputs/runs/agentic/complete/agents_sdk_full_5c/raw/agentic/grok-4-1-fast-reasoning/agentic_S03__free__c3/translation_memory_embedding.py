import os
from openai import OpenAI
from typing import List, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_translated_segments(segments: List[str]) -> List[Any]:
    \"\"\"Generate embeddings for translated segments.\"\"\"
    response = client.embeddings.create(
        input=segments,
        model="text-embedding-3-small"
    )
    return [data.embedding for data in response.data]