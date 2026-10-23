from model_client import openai_client
from model_models import parse_openai_embedding
from typing import List


def get_output_embedding(text: str) -> List[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return parse_openai_embedding(response)
