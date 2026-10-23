import os
from typing import Dict, List

from openai import OpenAI


def embed_asset_metadata(
    metadata: Dict[str, str], extracted_text: str, model: str = "text-embedding-3-large"
) -> List[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload = (
        "\n".join([f"{k}: {v}" for k, v in sorted(metadata.items())])
        + "\n\n"
        + extracted_text
    )
    result = client.embeddings.create(model=model, input=payload)
    return result.data[0].embedding
