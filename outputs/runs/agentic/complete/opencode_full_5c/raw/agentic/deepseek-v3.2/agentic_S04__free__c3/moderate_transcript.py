import os
from typing import List, Dict, Any
from openai import OpenAI
from speech_models import NormalizedTranscript


def moderate_transcript(transcript: NormalizedTranscript) -> Dict[str, Any]:
    """
    Moderate transcript text before publishing using OpenAI Moderation API.

    Args:
        transcript: Normalized transcript to moderate

    Returns:
        Dictionary with moderation results and flagged content
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=openai_api_key)

    chunks = split_into_chunks_for_moderation(transcript)
    all_results = {
        "flagged": False,
        "categories": {},
        "flagged_segments": [],
        "scores": {},
    }

    for i, chunk in enumerate(chunks):
        try:
            response = client.moderations.create(
                input=chunk, model="text-moderation-latest"
            )
            result = response.results[0]

            if result.flagged:
                all_results["flagged"] = True

                for category, flagged in result.categories.model_dump().items():
                    if flagged:
                        all_results["categories"][category] = True
                        score = result.category_scores.model_dump().get(category, 0.0)
                        all_results["scores"][category] = max(
                            all_results["scores"].get(category, 0.0), score
                        )

                all_results["flagged_segments"].append(
                    {
                        "chunk_index": i,
                        "text": chunk[:200] + "..." if len(chunk) > 200 else chunk,
                        "categories": [
                            cat
                            for cat, flagged in result.categories.model_dump().items()
                            if flagged
                        ],
                    }
                )

        except Exception as e:
            raise Exception(f"OpenAI Moderation API error: {e}")

    return all_results


def split_into_chunks_for_moderation(
    transcript: NormalizedTranscript, max_chars: int = 2000
) -> List[str]:
    """
    Split transcript into chunks suitable for moderation API.

    Args:
        transcript: Normalized transcript
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    text = transcript.text
    if len(text) <= max_chars:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) + 2 <= max_chars:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk)

            if len(paragraph) > max_chars:
                sentences = paragraph.split(". ")
                sub_chunk = ""
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue

                    if sentence[-1] != ".":
                        sentence += "."

                    if len(sub_chunk) + len(sentence) + 2 <= max_chars:
                        sub_chunk += " " + sentence if sub_chunk else sentence
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        sub_chunk = sentence

                if sub_chunk:
                    current_chunk = sub_chunk
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def moderate_with_context(
    transcript: NormalizedTranscript, context_categories: List[str] = None
) -> Dict[str, Any]:
    """
    Moderate transcript with specific context categories.

    Args:
        transcript: Normalized transcript
        context_categories: Specific categories to check (default: all)

    Returns:
        Detailed moderation results
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=openai_api_key)

    full_text = transcript.text

    try:
        response = client.moderations.create(
            input=full_text, model="text-moderation-latest"
        )
        result = response.results[0]

        moderation_result = {
            "flagged": result.flagged,
            "categories": {},
            "category_scores": {},
            "overall_score": max(result.category_scores.model_dump().values())
            if result.flagged
            else 0.0,
        }

        for category, flagged in result.categories.model_dump().items():
            if context_categories is None or category in context_categories:
                moderation_result["categories"][category] = flagged
                if flagged:
                    moderation_result["category_scores"][category] = (
                        result.category_scores.model_dump()[category]
                    )

        return moderation_result

    except Exception as e:
        raise Exception(f"OpenAI Moderation API error: {e}")
