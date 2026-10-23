from typing import List

from google import genai

from safety_client import configure_client, load_config


def embed_moderation_rationale(text: str) -> List[float]:
    cfg = configure_client(load_config())
    client = genai.Client(api_key=cfg.api_key)
    result = client.models.embed_content(model=cfg.embed_model, contents=text)
    return list(getattr(result, "embeddings", [])[0].values) if getattr(result, "embeddings", None) else []
