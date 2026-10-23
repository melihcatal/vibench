import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class EmbeddingSegment:
    text: str
    embedding: List[float]
    language: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class TranslationMemoryIndex:
    segments: List[EmbeddingSegment] = field(default_factory=list)
    dimension: int = 0
    model_used: str = ""


def embed_translation_segments(
    segments: List[str],
    languages: Optional[List[str]] = None,
    metadata_list: Optional[List[Dict]] = None,
    model: str = "text-embedding-3-small",
) -> TranslationMemoryIndex:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    if languages is None:
        languages = [""] * len(segments)
    if metadata_list is None:
        metadata_list = [{}] * len(segments)

    response = client.embeddings.create(
        model=model,
        input=segments,
        encoding_format="float",
    )

    embedded_segments = []
    dimension = 0

    for i, emb_data in enumerate(response.data):
        embedding = emb_data.embedding
        if dimension == 0:
            dimension = len(embedding)

        segment = EmbeddingSegment(
            text=segments[i],
            embedding=embedding,
            language=languages[i] if i < len(languages) else "",
            metadata=metadata_list[i] if i < len(metadata_list) else {},
        )
        embedded_segments.append(segment)

    return TranslationMemoryIndex(
        segments=embedded_segments,
        dimension=dimension,
        model_used=model,
    )


def search_translation_memory(
    query: str,
    index: TranslationMemoryIndex,
    top_k: int = 5,
    model: str = "text-embedding-3-small",
) -> List[Dict]:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    query_response = client.embeddings.create(
        model=model,
        input=query,
        encoding_format="float",
    )
    query_embedding = query_response.data[0].embedding

    query_vec = np.array(query_embedding)
    similarities = []

    for segment in index.segments:
        seg_vec = np.array(segment.embedding)
        norm_q = np.linalg.norm(query_vec)
        norm_s = np.linalg.norm(seg_vec)
        if norm_q > 0 and norm_s > 0:
            similarity = float(np.dot(query_vec, seg_vec) / (norm_q * norm_s))
        else:
            similarity = 0.0
        similarities.append((similarity, segment))

    similarities.sort(key=lambda x: x[0], reverse=True)
    top_results = similarities[:top_k]

    results = []
    for similarity, segment in top_results:
        results.append(
            {
                "text": segment.text,
                "similarity": similarity,
                "language": segment.language,
                "metadata": segment.metadata,
            }
        )

    return results
