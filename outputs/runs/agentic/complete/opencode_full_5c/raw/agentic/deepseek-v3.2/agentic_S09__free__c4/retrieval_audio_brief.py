import os
from typing import List, Dict, Any
from openai import OpenAI


def retrieval_audio_brief(
    search_results: List[Dict[str, Any]], query: str
) -> Dict[str, Any]:
    """
    Generate a spoken brief from retrieved search results using OpenAI's audio API.

    Args:
        search_results: List of search result dictionaries with 'text' and 'score' keys
        query: The original search query

    Returns:
        Dictionary with audio file information and transcript
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Prepare summary text from search results
    top_results = sorted(search_results, key=lambda x: x.get("score", 0), reverse=True)[
        :3
    ]

    summary_parts = [f"Search query: {query}"]
    summary_parts.append(
        f"Found {len(search_results)} results. Top {len(top_results)} most relevant:"
    )

    for i, result in enumerate(top_results, 1):
        text = result.get("text", "")
        score = result.get("score", 0)
        preview = text[:150] + "..." if len(text) > 150 else text
        summary_parts.append(f"Result {i} (relevance score: {score:.3f}): {preview}")

    summary_text = "\n".join(summary_parts)

    # Generate audio brief using OpenAI TTS
    try:
        speech_response = client.audio.speech.create(
            model="tts-1", voice="alloy", input=summary_text, response_format="mp3"
        )

        # Save audio to file
        audio_filename = f"search_brief_{hash(query) % 10000}.mp3"
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(speech_response.content)

        # Generate transcript using Whisper (optional)
        try:
            with open(audio_filename, "rb") as audio_file:
                transcript_response = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, response_format="text"
                )
            transcript = transcript_response
        except Exception as e:
            transcript = f"Transcript generation failed: {str(e)}"

        result = {
            "query": query,
            "num_results": len(search_results),
            "audio_file": audio_filename,
            "audio_format": "mp3",
            "voice": "alloy",
            "tts_model": "tts-1",
            "transcript": transcript,
            "summary_text": summary_text,
            "provider": "openai",
            "metadata": {
                "top_scores": [r.get("score", 0) for r in top_results],
                "audio_size_bytes": os.path.getsize(audio_filename)
                if os.path.exists(audio_filename)
                else 0,
            },
        }

    except Exception as e:
        result = {
            "query": query,
            "num_results": len(search_results),
            "error": str(e),
            "provider": "openai",
            "summary_text": summary_text,
        }

    return result
