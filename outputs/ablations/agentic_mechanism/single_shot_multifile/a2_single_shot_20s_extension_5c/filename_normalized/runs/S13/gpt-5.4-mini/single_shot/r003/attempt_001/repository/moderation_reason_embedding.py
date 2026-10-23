from typing import Dict, List

from openai import OpenAI

from safety_client import load_safety_config


def moderation_reason_embedding(text: str) -> Dict[str, List[float]]:
    config = load_safety_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    embedding = response.data[0].embedding if response.data else []
    return {"embedding": embedding, "model": "text-embedding-3-small"}
