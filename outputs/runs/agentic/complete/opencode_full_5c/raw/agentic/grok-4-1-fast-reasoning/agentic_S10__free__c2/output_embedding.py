from model_client import get_openai_client
from typing import List, Union


def output_embedding(text: Union[str, List[str]]) -> List[List[float]]:
    client = get_openai_client()
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return [[float(v) for v in data.embedding] for data in resp.data]
