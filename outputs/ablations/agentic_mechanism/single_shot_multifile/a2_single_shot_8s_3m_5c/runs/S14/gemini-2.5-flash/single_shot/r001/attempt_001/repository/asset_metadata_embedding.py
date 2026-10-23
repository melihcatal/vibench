import os
from typing import List
from openai import OpenAI
from storage_models import EmbeddingResponse

def get_text_embedding(text_content: str) -> EmbeddingResponse:
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    model_id = "text-embedding-3-small"

    response = client.embeddings.create(
        input=text_content,
        model=model_id
    )
    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
