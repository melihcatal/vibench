from typing import Any, Dict, List

from model_client import build_platform_client, get_config



def platform_output_embedding(text: str, **kwargs: Any) -> Dict[str, Any]:
    config = get_config()
    client = build_platform_client(config)
    if config.provider == "openai":
        response = client.embeddings.create(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"), input=text, **kwargs)
        embedding: List[float] = response.data[0].embedding
        return {"embedding": embedding, "response": response, "model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")}
    if config.provider == "anthropic":
        raise RuntimeError("Anthropic does not provide embeddings in the same API; configure PLATFORM_PROVIDER=openai")
    raise RuntimeError(f"Unsupported provider: {config.provider}")
