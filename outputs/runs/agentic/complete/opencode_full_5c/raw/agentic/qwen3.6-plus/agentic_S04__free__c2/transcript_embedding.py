import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionResult,
    EmbeddingResult,
    OpenAIConfig,
)
from speech_client import (
    call_openai_api,
    get_openai_config,
    poll_until_complete,
    get_assemblyai_config,
)


def embed_transcript_segments(
    segments: List[Dict[str, Any]],
    text_key: str = "text",
    config: Optional[OpenAIConfig] = None,
    batch_size: int = 100,
) -> EmbeddingResult:
    if config is None:
        config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    texts = [seg.get(text_key, "") for seg in segments if seg.get(text_key)]
    if not texts:
        return EmbeddingResult(segments=[], model=config.embedding_model)
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        payload = {
            "input": batch,
            "model": config.embedding_model,
        }
        response = call_openai_api("embeddings", payload, config)
        batch_data = response.get("data", [])
        all_embeddings.extend(batch_data)
    enriched_segments = []
    for idx, seg in enumerate(segments):
        enriched = dict(seg)
        if idx < len(all_embeddings):
            enriched["embedding"] = all_embeddings[idx].get("embedding")
            enriched["embedding_index"] = all_embeddings[idx].get("index")
        enriched_segments.append(enriched)
    return EmbeddingResult(
        segments=enriched_segments,
        model=config.embedding_model,
        total_segments=len(enriched_segments),
    )


def embed_completed_transcript(
    job_id: str,
    use_utterances: bool = True,
    batch_size: int = 100,
) -> EmbeddingResult:
    assemblyai_config = get_assemblyai_config()
    transcription = poll_until_complete(job_id, assemblyai_config)
    if use_utterances:
        segments = [
            {
                "text": u.text,
                "speaker": u.speaker,
                "start_ms": u.start,
                "end_ms": u.end,
            }
            for u in transcription.utterances
        ]
    else:
        segments = [
            {
                "text": w.text,
                "start_ms": w.start,
                "end_ms": w.end,
            }
            for w in transcription.words
        ]
    return embed_transcript_segments(segments, batch_size=batch_size)


def search_similar_segments(
    query: str,
    embedded_segments: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    query_payload = {
        "input": query,
        "model": config.embedding_model,
    }
    query_response = call_openai_api("embeddings", query_payload, config)
    query_embedding = query_response.get("data", [{}])[0].get("embedding")
    if not query_embedding:
        return []
    scored_segments = []
    for seg in embedded_segments:
        embedding = seg.get("embedding")
        if embedding and len(embedding) == len(query_embedding):
            dot_product = sum(a * b for a, b in zip(query_embedding, embedding))
            scored_segments.append(
                {
                    **seg,
                    "similarity_score": round(dot_product, 6),
                }
            )
    scored_segments.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
    return scored_segments[:top_k]


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcript_embedding.py <job_id> [query]")
        sys.exit(1)
    job_id = sys.argv[1]
    query = sys.argv[2] if len(sys.argv) > 2 else None
    result = embed_completed_transcript(job_id)
    if query:
        similar = search_similar_segments(query, result.segments, top_k=5)
        output = {
            "query": query,
            "model": result.model,
            "total_segments": result.total_segments,
            "top_matches": similar,
        }
    else:
        output = {
            "model": result.model,
            "total_segments": result.total_segments,
            "segments": [
                {
                    "text": s.get("text", ""),
                    "speaker": s.get("speaker"),
                    "start_ms": s.get("start_ms"),
                    "end_ms": s.get("end_ms"),
                    "embedding_dimension": len(s.get("embedding", []))
                    if s.get("embedding")
                    else 0,
                }
                for s in result.segments
            ],
        }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
