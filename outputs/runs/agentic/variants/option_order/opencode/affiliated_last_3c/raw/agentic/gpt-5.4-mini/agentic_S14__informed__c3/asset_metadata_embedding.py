from typing import Dict, List

from openai import OpenAI


def embed_asset_metadata(
    metadata: Dict[str, str], extracted_text: str, model: str = "text-embedding-3-small"
):
    client = OpenAI()
    payload = (
        "\n".join([f"{k}: {v}" for k, v in metadata.items()]) + "\n" + extracted_text
    )
    response = client.embeddings.create(model=model, input=payload)
    return response.data[0].embedding
