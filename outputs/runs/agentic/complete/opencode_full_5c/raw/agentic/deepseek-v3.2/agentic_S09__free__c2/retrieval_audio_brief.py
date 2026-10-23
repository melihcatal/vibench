import os
from typing import List, Dict, Any
from openai import OpenAI
import json


def generate_audio_brief(
    search_results: List[Dict[str, Any]], model: str = "tts-1"
) -> Dict[str, Any]:
    """
    Generate a spoken audio brief from retrieved search results using OpenAI's Text-to-Speech API.

    Args:
        search_results: List of search results with document text and similarity scores
        model: The OpenAI TTS model to use (default: tts-1)

    Returns:
        Dict containing audio brief information
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Prepare brief text from search results
    if not search_results:
        brief_text = "No search results found."
    else:
        # Sort by similarity score (descending)
        sorted_results = sorted(
            search_results, key=lambda x: x.get("similarity", 0), reverse=True
        )

        # Take top 3 results
        top_results = sorted_results[:3]

        # Generate brief summary
        brief_parts = []
        brief_parts.append(
            f"Found {len(search_results)} relevant documents. Here are the top {len(top_results)} results:"
        )

        for i, result in enumerate(top_results, 1):
            similarity = result.get("similarity", 0)
            document_preview = result.get("document", "")[:100]
            if len(result.get("document", "")) > 100:
                document_preview += "..."

            brief_parts.append(
                f"Result {i} with {similarity:.2f} similarity: {document_preview}"
            )

        brief_parts.append("End of search results brief.")
        brief_text = " ".join(brief_parts)

    try:
        # Generate speech using OpenAI TTS
        response = client.audio.speech.create(
            model=model,
            voice="alloy",  # OpenAI TTS voice
            input=brief_text,
            response_format="mp3",
        )

        # Save audio to file
        audio_filename = f"search_brief_{len(search_results)}_results.mp3"
        response.stream_to_file(audio_filename)

        # Generate additional metadata
        metadata = {
            "brief_text": brief_text,
            "audio_file": audio_filename,
            "model_used": model,
            "voice_used": "alloy",
            "total_results": len(search_results),
            "top_results_summarized": min(3, len(search_results)),
            "audio_duration_estimate": len(brief_text)
            / 15,  # Rough estimate: 15 chars per second
            "provider": "OpenAI",
            "tts_api": "audio.speech.create",
        }

        return metadata

    except Exception as e:
        # Fallback: return text brief if audio generation fails
        return {
            "brief_text": brief_text,
            "audio_generation_failed": True,
            "error": str(e),
            "fallback_available": True,
            "provider": "OpenAI",
        }


def create_search_results_audio(
    search_query: str, documents: List[str], similarity_scores: List[float]
) -> Dict[str, Any]:
    """
    Create audio brief from search query and results.

    Args:
        search_query: The original search query
        documents: List of document strings
        similarity_scores: List of similarity scores

    Returns:
        Dict containing audio brief information
    """
    # Prepare search results
    search_results = []
    for i, (doc, score) in enumerate(zip(documents, similarity_scores)):
        search_results.append(
            {
                "index": i,
                "document": doc,
                "similarity": score,
                "document_preview": doc[:150] + "..." if len(doc) > 150 else doc,
            }
        )

    # Generate audio brief
    audio_brief = generate_audio_brief(search_results)

    # Add search context
    audio_brief.update(
        {
            "search_query": search_query,
            "total_documents": len(documents),
            "avg_similarity": sum(similarity_scores) / len(similarity_scores)
            if similarity_scores
            else 0,
            "max_similarity": max(similarity_scores) if similarity_scores else 0,
        }
    )

    return audio_brief
