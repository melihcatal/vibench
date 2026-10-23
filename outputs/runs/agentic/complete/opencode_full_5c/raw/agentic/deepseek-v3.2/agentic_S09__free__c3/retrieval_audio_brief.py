import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
import tempfile
import base64


def generate_audio_brief_from_results(
    search_results: List[Dict[str, Any]],
    query: str,
    max_results: int = 3,
    voice: str = "alloy",
) -> Dict[str, Any]:
    """
    Generate a spoken audio brief from retrieved search results using OpenAI's TTS API.

    Args:
        search_results: List of search result dictionaries with 'document' and 'similarity_score' keys
        query: Original search query
        max_results: Maximum number of results to include in brief
        voice: TTS voice to use (alloy, echo, fable, onyx, nova, shimmer)

    Returns:
        Dict with audio brief information
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Sort results by similarity score (descending)
    sorted_results = sorted(
        search_results, key=lambda x: x.get("similarity_score", 0), reverse=True
    )

    # Take top results
    top_results = sorted_results[:max_results]

    # Create brief text
    brief_parts = []
    brief_parts.append(
        f"Here are the top {len(top_results)} results for your query: '{query}'"
    )

    for i, result in enumerate(top_results, 1):
        document = result.get("document", "")
        score = result.get("similarity_score", 0)

        # Extract first sentence or first 100 characters
        preview = document.split(".")[0] if "." in document else document[:100]
        if len(preview) < len(document):
            preview += "..."

        brief_parts.append(f"Result {i}, with {score:.1%} relevance: {preview}")

    brief_parts.append("End of search results brief.")

    brief_text = " ".join(brief_parts)

    # Generate audio using OpenAI TTS
    try:
        response = client.audio.speech.create(
            model="tts-1", voice=voice, input=brief_text
        )

        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            response.stream_to_file(tmp_file.name)
            audio_file_path = tmp_file.name

        # Read audio file as base64 for potential web delivery
        with open(audio_file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

        # Create transcript with timestamps (simulated)
        transcript = []
        current_time = 0
        for part in brief_parts:
            # Estimate duration: ~4 words per second
            word_count = len(part.split())
            duration = word_count / 4  # seconds

            transcript.append(
                {
                    "text": part,
                    "start": current_time,
                    "end": current_time + duration,
                    "duration": duration,
                }
            )

            current_time += duration

        result = {
            "query": query,
            "audio_file": audio_file_path,
            "audio_base64": audio_base64[:100] + "..."
            if len(audio_base64) > 100
            else audio_base64,
            "audio_format": "mp3",
            "voice": voice,
            "duration_seconds": current_time,
            "transcript": transcript,
            "brief_text": brief_text,
            "results_summary": {
                "total_results": len(search_results),
                "included_in_brief": len(top_results),
                "top_similarity_score": top_results[0].get("similarity_score", 0)
                if top_results
                else 0,
                "average_similarity_score": sum(
                    r.get("similarity_score", 0) for r in top_results
                )
                / max(len(top_results), 1),
            },
            "success": True,
        }

        return result

    except Exception as e:
        # Fallback: return text brief if audio generation fails
        return {
            "query": query,
            "audio_file": None,
            "brief_text": brief_text,
            "results_summary": {
                "total_results": len(search_results),
                "included_in_brief": len(top_results),
                "top_similarity_score": top_results[0].get("similarity_score", 0)
                if top_results
                else 0,
            },
            "success": False,
            "error": str(e),
            "fallback_available": True,
        }


def create_search_results_summary(
    search_results: List[Dict[str, Any]], query: str
) -> str:
    """
    Create a text summary of search results for audio generation.

    Args:
        search_results: List of search results
        query: Original query

    Returns:
        str: Text summary
    """
    if not search_results:
        return f"No results found for query: '{query}'"

    sorted_results = sorted(
        search_results, key=lambda x: x.get("similarity_score", 0), reverse=True
    )
    top_results = sorted_results[:3]

    summary_parts = []
    summary_parts.append(f"Found {len(search_results)} results for '{query}'. ")
    summary_parts.append(
        f"Top result has {top_results[0].get('similarity_score', 0):.1%} similarity. "
    )

    if len(top_results) > 1:
        summary_parts.append(
            f"Second result: {top_results[1].get('document', '')[:50]}... "
        )

    return "".join(summary_parts)


def embed_and_generate_audio_brief(
    query: str,
    documents: List[str],
    model: str = "text-embedding-3-small",
    voice: str = "alloy",
) -> Dict[str, Any]:
    """
    Complete pipeline: embed query and documents, perform search, generate audio brief.

    Args:
        query: Search query
        documents: List of documents to search
        model: Embedding model to use
        voice: TTS voice to use

    Returns:
        Dict with complete pipeline results
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Step 1: Embed query and documents
    query_response = client.embeddings.create(
        model=model, input=query, encoding_format="float"
    )
    query_embedding = query_response.data[0].embedding

    doc_response = client.embeddings.create(
        model=model, input=documents, encoding_format="float"
    )
    document_embeddings = [item.embedding for item in doc_response.data]

    # Step 2: Calculate similarities
    import numpy as np

    query_vec = np.array(query_embedding)

    search_results = []
    for i, (doc, doc_embedding) in enumerate(zip(documents, document_embeddings)):
        doc_vec = np.array(doc_embedding)
        dot_product = np.dot(query_vec, doc_vec)
        norm_query = np.linalg.norm(query_vec)
        norm_doc = np.linalg.norm(doc_vec)

        if norm_query == 0 or norm_doc == 0:
            similarity = 0.0
        else:
            similarity = float(dot_product / (norm_query * norm_doc))

        search_results.append(
            {
                "document": doc,
                "similarity_score": similarity,
                "index": i,
                "embedding": doc_embedding,
            }
        )

    # Step 3: Generate audio brief
    audio_brief = generate_audio_brief_from_results(
        search_results=search_results, query=query, max_results=3, voice=voice
    )

    # Combine all results
    pipeline_result = {
        "pipeline_steps": ["embedding", "similarity_calculation", "audio_generation"],
        "embedding_model": model,
        "query": query,
        "documents_count": len(documents),
        "search_results_count": len(search_results),
        "audio_brief": audio_brief,
        "top_results": sorted(
            search_results, key=lambda x: x["similarity_score"], reverse=True
        )[:5],
        "embedding_usage": {
            "query_tokens": query_response.usage.prompt_tokens,
            "documents_tokens": doc_response.usage.prompt_tokens,
            "total_tokens": query_response.usage.total_tokens
            + doc_response.usage.total_tokens,
        },
    }

    return pipeline_result
