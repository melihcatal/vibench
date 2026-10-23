from model_client import create_openai_client, load_config, resolve_model
from model_models import EmbedRequest, EmbedResponse


def embed_texts(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> EmbedResponse:
    req = EmbedRequest(texts=texts, model=model, dimensions=dimensions)
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    params = {
        "input": req.texts,
        "model": resolved_model,
    }
    if req.dimensions is not None:
        params["dimensions"] = req.dimensions

    response = client.embeddings.create(**params)

    embeddings = [item.embedding for item in response.data]
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return EmbedResponse(
        embeddings=embeddings,
        model=response.model,
        usage=usage,
    )


def embed_single(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> list[float]:
    result = embed_texts([text], model=model, dimensions=dimensions)
    return result.embeddings[0] if result.embeddings else []


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    import sys
    import json

    input_texts = []
    for line in sys.stdin:
        stripped = line.strip()
        if stripped:
            input_texts.append(stripped)

    if input_texts:
        result = embed_texts(input_texts)
        print(json.dumps(result.embeddings, indent=2))
