from typing import List
from model_client import get_openai_client
from model_models import EmbeddingInput, EmbeddingOutput

def get_embedding(input_data: EmbeddingInput) -> EmbeddingOutput:
    client = get_openai_client()
    response = client.embeddings.create(
        model=input_data.model_name,
        input=[input_data.text]
    )
    if response.data:
        return EmbeddingOutput(
            embedding=response.data[0].embedding,
            model_name=input_data.model_name
        )
    raise ValueError("Failed to generate embedding.")