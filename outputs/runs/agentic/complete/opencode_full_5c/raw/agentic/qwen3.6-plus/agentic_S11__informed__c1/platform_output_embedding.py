from typing import Optional

import dashscope
from dashscope import TextEmbedding

from model_client import configure_dashscope_client, DEFAULT_EMBEDDING_MODEL
from model_models import EmbeddingResult, PlatformUsage


def embed_platform_outputs(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    text_type: str = "query",
) -> EmbeddingResult:
    configure_dashscope_client()

    response = TextEmbedding.call(
        model=model,
        input=texts,
        text_type=text_type,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope / Alibaba Model Studio embedding error: "
            f"code={response.code}, message={response.message}"
        )

    output = response.output
    embeddings_data = output.get("embeddings", [])
    embeddings = []
    for item in embeddings_data:
        embedding_vec = item.get("embedding", [])
        embeddings.append(embedding_vec)

    usage_data = getattr(response, "usage", None)
    if isinstance(usage_data, dict):
        usage = PlatformUsage.from_dashscope(usage_data)
    else:
        usage = PlatformUsage()

    return EmbeddingResult(
        embeddings=embeddings,
        model_id=getattr(response, "model", model),
        request_id=getattr(response, "request_id", ""),
        usage=usage,
        raw_response=response,
    )


def embed_single_platform_output(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    text_type: str = "query",
) -> EmbeddingResult:
    return embed_platform_outputs(
        texts=[text],
        model=model,
        text_type=text_type,
    )


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)
