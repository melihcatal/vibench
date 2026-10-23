"""Generate a spoken brief from retrieved search results using OpenAI TTS API."""

import os
from typing import List, Dict, Optional, Any
import base64
from openai import OpenAI

from embeddings_client import get_openai_client


def generate_audio_brief(
    search_results: List[Dict],
    query: str = "",
    voice: str = "alloy",
    model: str = "tts-1",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> Dict[str, Any]:
    """Generate a spoken audio brief from semantic search results.

    Uses OpenAI's text-to-speech API (tts-1 model) to create an audio summary
    of search results retrieved via OpenAI embeddings.

    Args:
        search_results: List of search result dicts with 'document' and 'score' keys.
        query: The original search query.
        voice: OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer).
        model: OpenAI TTS model (tts-1 or tts-1-hd).
        response_format: Audio format (mp3, opus, aac, flac, wav, pcm).
        speed: Playback speed (0.25 to 4.0).

    Returns:
        Dict with audio data, transcript, and metadata.
    """
    client = get_openai_client()

    # Generate summary script for TTS
    summary_script = _create_brief_script(query, search_results)

    # Generate audio using OpenAI TTS
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=summary_script,
        response_format=response_format,
        speed=speed,
    )

    audio_bytes = response.content
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio_base64": audio_base64,
        "audio_format": response_format,
        "transcript": summary_script,
        "result_count": len(search_results),
        "voice": voice,
        "model": model,
        "provider": "OpenAI",
        "api_endpoint": "https://api.openai.com/v1/audio/speech",
    }


def _create_brief_script(
    query: str,
    search_results: List[Dict],
    max_results: int = 5,
) -> str:
    """Create a natural language script summarizing search results for TTS."""
    limited_results = search_results[:max_results]

    script_parts = []

    if query:
        script_parts.append(f"Here are the top results for: {query}")

    for i, result in enumerate(limited_results, 1):
        doc = result.get("document", "")
        score = result.get("score", 0.0)
        confidence = "high" if score > 0.7 else "medium" if score > 0.5 else "lower"

        script_parts.append(
            f"Result {i}, with {confidence} relevance: {doc}"
        )

    if len(search_results) > max_results:
        remaining = len(search_results) - max_results
        script_parts.append(
            f"There are {remaining} additional results available."
        )

    script_parts.append("End of brief.")
    return " ".join(script_parts)


def generate_audio_brief_from_texts(
    query: str,
    documents: List[str],
    scores: List[float],
    voice: str = "alloy",
    model: str = "tts-1-hd",
    response_format: str = "mp3",
    max_results: int = 3,
) -> Dict[str, Any]:
    """Generate audio brief directly from query, documents, and scores.

    Combines OpenAI embeddings-based retrieval scores with OpenAI TTS
    to produce an audio summary of search results.

    Args:
        query: The search query.
        documents: List of document texts.
        scores: List of relevance scores matching documents.
        voice: OpenAI TTS voice.
        model: OpenAI TTS model.
        response_format: Audio output format.
        max_results: Maximum results to include in brief.

    Returns:
        Audio brief dictionary.
    """
    # Pair and sort by score
    paired = list(zip(documents, scores))
    paired.sort(key=lambda x: x[1], reverse=True)

    search_results = [
        {"document": doc, "score": float(score)}
        for doc, score in paired[:max_results]
    ]

    return generate_audio_brief(
        search_results=search_results,
        query=query,
        voice=voice,
        model=model,
        response_format=response_format,
    )


def save_audio_brief(
    audio_data: Dict[str, Any],
    output_path: str,
) -> str:
    """Save audio brief to a file.

    Args:
        audio_data: Audio brief dict from generate_audio_brief.
        output_path: File path to save audio.

    Returns:
        The output path.
    """
    audio_bytes = base64.b64decode(audio_data["audio_base64"])
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def create_search_and_brief_pipeline(
    query: str,
    documents: List[str],
    embedding_model: str = "text-embedding-3-small",
    tts_model: str = "tts-1",
    voice: str = "alloy",
    top_k: int = 5,
) -> Dict[str, Any]:
    """Full pipeline: embed search, retrieve results, and generate audio brief.

    Uses OpenAI text-embedding-3-small for semantic retrieval and
    OpenAI tts-1 for audio generation.

    Args:
        query: Search query.
        documents: Document corpus.
        embedding_model: OpenAI embedding model.
        tts_model: OpenAI TTS model.
        voice: TTS voice name.
        top_k: Number of results to retrieve and summarize.

    Returns:
        Pipeline results with search results and audio brief.
    """
    from embed_for_search import embed_for_search

    # Step 1: Semantic search using OpenAI embeddings
    search_results = embed_for_search(
        query=query,
        documents=documents,
        model=embedding_model,
        top_k=top_k,
    )

    # Step 2: Generate audio brief using OpenAI TTS
    audio_brief = generate_audio_brief(
        search_results=search_results,
        query=query,
        voice=voice,
        model=tts_model,
    )

    return {
        "query": query,
        "search_results": search_results,
        "audio_brief": audio_brief,
        "models_used": {
            "embedding": embedding_model,
            "tts": tts_model,
        },
        "provider": "OpenAI",
    }


if __name__ == "__main__":
    sample_docs = [
        "OpenAI's GPT-4 model demonstrates advanced reasoning capabilities.",
        "The company released new embedding models with improved performance.",
        "Audio generation APIs are becoming more accessible to developers.",
        "Machine learning continues to advance in multiple domains.",
    ]

    pipeline = create_search_and_brief_pipeline(
        query="What new AI models has OpenAI released?",
        documents=sample_docs,
        top_k=3,
    )

    print(f"Query: {pipeline['query']}")
    print(f"Results found: {len(pipeline['search_results'])}")
    print(f"Audio brief transcript:\n{pipeline['audio_brief']['transcript']}")
    print(f"Audio format: {pipeline['audio_brief']['audio_format']}")
    print(f"Models: {pipeline['models_used']}")
