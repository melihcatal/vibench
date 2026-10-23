from model_client import get_llm_client, get_model_id
from typing import List


def get_output_embedding(
    text: str, model_family: str = "text-embedding-3-small"
) -> List[float]:
    client = get_llm_client()
    model = get_model_id(model_family)
    response = client.embeddings.create(input=text, model=model)
    return list(response.data[0].embedding)
