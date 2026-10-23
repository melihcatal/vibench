import os
from typing import List, Dict, Any
from gtts import gTTS
import tempfile
from pathlib import Path


def generate_audio_brief(
    search_results: List[Dict[str, Any]], language: str = "en"
) -> str:
    """
    Generate a spoken brief from retrieved search results using Google Text-to-Speech.
    """
    if not search_results:
        return "No search results to summarize."

    # Create a summary text from search results
    summary_text = (
        f"Search results summary. Found {len(search_results)} relevant items. "
    )

    for i, result in enumerate(search_results[:3], 1):
        title = result.get("title", "Untitled")
        snippet = result.get("snippet", "")[:100]
        score = result.get("score", 0)

        summary_text += f"Result {i}: {title}. "
        if snippet:
            summary_text += f"Relevant content: {snippet}. "
        summary_text += f"Relevance score: {score:.2f}. "

    if len(search_results) > 3:
        summary_text += f"Plus {len(search_results) - 3} more results. "

    summary_text += "End of search results summary."

    # Generate audio using gTTS
    tts = gTTS(text=summary_text, lang=language, slow=False)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        audio_path = tmp_file.name
        tts.save(audio_path)

    return audio_path


def create_search_result_summary(search_results: List[Dict[str, Any]]) -> str:
    """
    Create a text summary of search results for audio generation.
    """
    if not search_results:
        return "No search results found."

    summary_parts = []
    summary_parts.append(f"Found {len(search_results)} relevant documents.")

    top_results = sorted(search_results, key=lambda x: x.get("score", 0), reverse=True)[
        :3
    ]

    for i, result in enumerate(top_results, 1):
        title = result.get("title", "Document")
        snippet = result.get("snippet", "")
        score = result.get("score", 0)

        summary_parts.append(f"Top result {i}: {title}")
        if snippet:
            # Clean snippet for speech
            clean_snippet = snippet.replace("\n", " ").replace("  ", " ")[:150]
            summary_parts.append(f"Contains: {clean_snippet}")
        summary_parts.append(f"Relevance: {score:.1f} out of 1.0")

    if len(search_results) > 3:
        summary_parts.append(
            f"Plus {len(search_results) - 3} additional relevant documents."
        )

    return " ".join(summary_parts)
