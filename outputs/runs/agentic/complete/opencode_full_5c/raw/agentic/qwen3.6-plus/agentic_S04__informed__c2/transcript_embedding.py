import dashscope
from dashscope import TextEmbedding

from speech_client import load_dashscope_config
from speech_models import (
    EmbeddingResult,
    EmbeddingSegment,
    normalize_dashscope_embedding,
)


def embed_transcript_segments(
    segments: list, model: str = None, dimensions: int = None
) -> EmbeddingResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    model_name = model or config.default_embedding_model

    texts = []
    for seg in segments:
        if isinstance(seg, dict):
            texts.append(seg.get("text", seg.get("original_text", "")))
        else:
            texts.append(seg.text if hasattr(seg, "text") else str(seg))

    response = TextEmbedding.call(
        model=model_name,
        input=texts,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embeddings API error: {response.code} - {response.message}"
        )

    raw_output = response.output
    embeddings_data = raw_output.get("embeddings", [])

    result_segments = []
    for idx, emb_item in enumerate(embeddings_data):
        result_segments.append(
            EmbeddingSegment(
                text=emb_item.get("text", ""),
                embedding=emb_item.get("embedding", []),
                segment_index=idx,
            )
        )

    return EmbeddingResult(
        segments=result_segments,
        model=model_name,
        dimensions=len(result_segments[0].embedding) if result_segments else 0,
    )


def embed_full_transcript(text: str, model: str = None) -> EmbeddingResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    model_name = model or config.default_embedding_model

    response = TextEmbedding.call(
        model=model_name,
        input=text,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embeddings API error: {response.code} - {response.message}"
        )

    raw_output = response.output
    embeddings_data = raw_output.get("embeddings", [])

    result_segments = []
    for idx, emb_item in enumerate(embeddings_data):
        result_segments.append(
            EmbeddingSegment(
                text=emb_item.get("text", ""),
                embedding=emb_item.get("embedding", []),
                segment_index=idx,
            )
        )

    return EmbeddingResult(
        segments=result_segments,
        model=model_name,
        dimensions=len(result_segments[0].embedding) if result_segments else 0,
    )


def embed_with_dimensions(texts: list, dimensions: int = 1536) -> EmbeddingResult:
    config = load_dashscope_config()
    dashscope.api_key = config.api_key

    response = TextEmbedding.call(
        model="text-embedding-v3",
        input=texts,
        dimensions=dimensions,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embeddings API error: {response.code} - {response.message}"
        )

    raw_output = response.output
    embeddings_data = raw_output.get("embeddings", [])

    result_segments = []
    for idx, emb_item in enumerate(embeddings_data):
        result_segments.append(
            EmbeddingSegment(
                text=emb_item.get("text", ""),
                embedding=emb_item.get("embedding", []),
                segment_index=idx,
            )
        )

    return EmbeddingResult(
        segments=result_segments,
        model="text-embedding-v3",
        dimensions=dimensions,
    )
