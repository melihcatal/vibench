"""
Generate a spoken brief from retrieved search results.

Provider: OpenAI Audio API (https://api.openai.com)
Model: gpt-4o-mini (for synthesis), tts-1 (for speech generation)
"""

import base64
import os
from typing import List, Optional, Dict, Any

from openai import OpenAI

from embeddings_client import get_openai_client


BRIEF_PROMPT_TEMPLATE = """\
You are an assistant generating a concise spoken brief from search results.
Summarize the following search results for the query: "{query}"

Search results:
{results_text}

Provide a brief, natural-sounding summary suitable for text-to-speech.
Keep it under 150 words. Do not include markdown, lists, or formatting.
Speak directly to the user in a conversational tone.
"""


class AudioBriefResult:
    """
    Result of generating an audio brief from search results.

    Attributes:
        query: Original search query
        results_count: Number of search results summarized
        brief_text: Generated brief text
        audio_content: Raw audio bytes from OpenAI TTS
        audio_format: Audio format (e.g., 'mp3')
        model: TTS model used
    """

    def __init__(
        self,
        query: str,
        results_count: int = 0,
        brief_text: str = "",
        audio_content: bytes = b"",
        audio_format: str = "mp3",
        model: str = "tts-1",
    ):
        self.query = query
        self.results_count = results_count
        self.brief_text = brief_text
        self.audio_content = audio_content
        self.audio_format = audio_format
        self.model = model

    @property
    def audio_base64(self) -> str:
        return base64.b64encode(self.audio_content).decode("utf-8")

    def save_audio(self, filepath: str) -> None:
        """Save the generated audio to a file."""
        with open(filepath, "wb") as f:
            f.write(self.audio_content)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "results_count": self.results_count,
            "brief_text": self.brief_text,
            "audio_format": self.audio_format,
            "audio_size_bytes": len(self.audio_content),
            "model": self.model,
        }


def generate_brief_text(
    query: str,
    search_results: List[Dict[str, Any]],
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> str:
    """
    Generate a spoken brief text from search results using OpenAI's chat API.

    Uses gpt-4o-mini to synthesize a conversational summary of search results.

    Args:
        query: Original search query
        search_results: List of search result dicts with 'document' and 'score'
        model: OpenAI chat model (default: gpt-4o-mini)
        api_key: OpenAI API key

    Returns:
        Generated brief text suitable for TTS
    """
    if not search_results:
        return "No results were found for your query."

    results_text = "\n".join(
        f"- {r.get('document', r.get('text', ''))} (relevance: {r.get('score', 0):.2f})"
        for r in search_results[:5]
    )

    prompt = BRIEF_PROMPT_TEMPLATE.format(
        query=query,
        results_text=results_text,
    )

    client = get_openai_client(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates concise spoken briefs from search results.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


def synthesize_audio(
    text: str,
    model: str = "tts-1",
    voice: str = "alloy",
    api_key: Optional[str] = None,
) -> bytes:
    """
    Synthesize audio from text using OpenAI's Text-to-Speech API.

    Uses OpenAI's tts-1 model to generate spoken audio from the brief text.

    Args:
        text: Text to synthesize
        model: OpenAI TTS model (default: tts-1)
        voice: Voice style (alloy, echo, fable, onyx, nova, shimmer)
        api_key: OpenAI API key

    Returns:
        Audio content as bytes (mp3 format)
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    client = get_openai_client(api_key=api_key)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format="mp3",
    )

    return response.content


def retrieval_audio_brief(
    query: str,
    search_results: List[Dict[str, Any]],
    synthesis_model: str = "tts-1",
    voice: str = "alloy",
    brief_model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> AudioBriefResult:
    """
    Generate a complete spoken audio brief from search results.

    First uses OpenAI's gpt-4o-mini to synthesize a conversational summary,
    then uses OpenAI's tts-1 model to generate spoken audio.

    Args:
        query: Original search query
        search_results: List of search result dicts
        synthesis_model: OpenAI TTS model (default: tts-1)
        voice: TTS voice style
        brief_model: OpenAI model for brief generation (default: gpt-4o-mini)
        api_key: OpenAI API key

    Returns:
        AudioBriefResult with brief text and audio content
    """
    brief_text = generate_brief_text(
        query=query,
        search_results=search_results,
        model=brief_model,
        api_key=api_key,
    )

    audio_content = synthesize_audio(
        text=brief_text,
        model=synthesis_model,
        voice=voice,
        api_key=api_key,
    )

    return AudioBriefResult(
        query=query,
        results_count=len(search_results),
        brief_text=brief_text,
        audio_content=audio_content,
        audio_format="mp3",
        model=synthesis_model,
    )


if __name__ == "__main__":
    import json

    sample_results = [
        {"document": "Machine learning uses data to train predictive models.", "score": 0.92},
        {"document": "Neural networks learn hierarchical representations.", "score": 0.85},
    ]
    brief = retrieval_audio_brief(
        query="What is machine learning?",
        search_results=sample_results,
    )
    print(json.dumps(brief.to_dict(), indent=2))
    print(f"Brief text: {brief.brief_text}")
