import os
from typing import List, Optional

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def embed_platform_outputs(outputs: List[str], model: Optional[str] = None) -> List[List[float]]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    chosen_model = model or OPENAI_EMBEDDING_MODEL
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": chosen_model, "input": outputs},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
