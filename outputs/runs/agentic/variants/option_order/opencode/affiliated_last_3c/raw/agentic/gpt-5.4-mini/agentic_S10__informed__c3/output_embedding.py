from typing import List

from model_client import get_client, pick_model


def output_embedding(text: str) -> List[float]:
    client = get_client()
    model = pick_model("embed")
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding
