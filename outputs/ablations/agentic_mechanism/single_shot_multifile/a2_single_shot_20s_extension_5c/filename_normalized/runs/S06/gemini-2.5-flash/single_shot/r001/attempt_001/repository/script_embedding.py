import os
from speech_client import get_openai_client
from speech_models import EmbeddingRequest
from typing import List

def embed_script(request: EmbeddingRequest) -> List[float]:
    openai_client = get_openai_client()
    response = openai_client.embeddings.create(
        input=[request.text],
        model=request.model
    )
    return response.data[0].embedding
