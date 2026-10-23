import os
from typing import Union, Dict, Any
from openai import OpenAI


def get_embeddings_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def create_embedding(
    client: OpenAI, model: str, input: Union[str, list[str]]
) -> Dict[str, Any]:
    response = client.embeddings.create(input=input, model=model)
    return response.model_dump()
