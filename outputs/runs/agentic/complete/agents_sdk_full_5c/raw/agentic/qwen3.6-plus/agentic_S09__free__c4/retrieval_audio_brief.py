"""
Generate a spoken brief from retrieved search results using OpenAI API.
Provider: OpenAI (api.openai.com)
Models: gpt-4o (brief generation), tts-1 (text-to-speech)
"""

from typing import List, Dict, Any, Optional
import io

from openai import OpenAI

from embeddings_client import get_openai_client, OPENAI_EMBEDDING_API_HOST


# Provider-specific model identifiers
OPENAI_BRIEF_GENERATION_MODEL = "gpt-4o"
OPENAI_TTS_MODEL = "tts-1"
OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_text_brief(
    query: str,
    search_results: List[Dict[str, Any]],
    max_length: int = 300,
    api_key: Optional[str] = None,
    model: str = OPENAI_BRIEF_GENERATION_MODEL,
) -> str:
    """
    Generate a concise text brief summarizing search results.

    Args:
        query: The original search query.
        search_results: List of search result dicts with 'document' and 'similarity_score'.
        max_length: Maximum length of the brief in characters.
        api_key: OpenAI API key.
        model: OpenAI model identifier for brief generation.

    Returns:
        Generated brief text.
    """
    client = get_openai_client(api_key=api_key)

    results_summary = "\n".join(
        f"- {r.get('document', '')} (relevance: {r.get('similarity_score', 0):.2f})"
        for r in search_results[:5]
    )

    system_prompt = (
        "You are a research assistant. Create a concise spoken brief summarizing "
        "the search results for the given query. Make it natural for text-to-speech. "
        f"Keep the response under {max_length} characters."
    )

    user_prompt = (
        f"Query: {query}\n\n"
        f"Search results:\n{results_summary}\n\n"
        f"Generate a brief spoken summary."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    brief_text = response.choices[0].message.content.strip()
    return brief_text


def generate_audio_brief(
    query: str,
    search_results: List[Dict[str, Any]],
    voice: str = "nova",
    max_length: int = 300,
    api_key: Optional[str] = None,
    model: str = OPENAI_TTS_MODEL,
) -> bytes:
    """
    Generate a spoken audio brief from search results using OpenAI TTS API.

    Args:
        query: The original search query.
        search_results: List of search result dicts.
        voice: OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer).
        max_length: Maximum length of the brief text.
        api_key: OpenAI API key.
        model: OpenAI TTS model identifier.

    Returns:
        Audio data as bytes (MP3 format).
    """
    if voice not in OPENAI_TTS_VOICES:
        raise ValueError(f"Invalid voice. Choose from: {OPENAI_TTS_VOICES}")

    brief_text = generate_text_brief(
        query, search_results, max_length=max_length, api_key=api_key
    )

    client = get_openai_client(api_key=api_key)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=brief_text,
        response_format="mp3",
    )

    audio_data = response.content
    return audio_data


def generate_audio_brief_to_file(
    query: str,
    search_results: List[Dict[str, Any]],
    output_path: str,
    voice: str = "nova",
    max_length: int = 300,
    api_key: Optional[str] = None,
) -> str:
    """
    Generate a spoken audio brief and save to file.

    Args:
        query: The original search query.
        search_results: List of search result dicts.
        output_path: File path to save the audio.
        voice: OpenAI TTS voice identifier.
        max_length: Maximum length of the brief text.
        api_key: OpenAI API key.

    Returns:
        Output file path.
    """
    audio_data = generate_audio_brief(
        query, search_results, voice=voice, max_length=max_length, api_key=api_key
    )

    with open(output_path, "wb") as f:
        f.write(audio_data)

    return output_path


def create_retrieval_brief_package(
    query: str,
    search_results: List[Dict[str, Any]],
    voice: str = "nova",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a complete brief package with text and audio.

    Args:
        query: The original search query.
        search_results: List of search result dicts.
        voice: OpenAI TTS voice.
        api_key: OpenAI API key.

    Returns:
        Dictionary with text_brief, audio_data, and metadata.
    """
    brief_text = generate_text_brief(query, search_results, api_key=api_key)

    audio_data = generate_audio_brief(
        query, search_results, voice=voice, api_key=api_key
    )

    return {
        "query": query,
        "text_brief": brief_text,
        "audio_data": audio_data,
        "audio_format": "mp3",
        "voice": voice,
        "result_count": len(search_results),
        "generation_model": OPENAI_BRIEF_GENERATION_MODEL,
        "tts_model": OPENAI_TTS_MODEL,
        "provider": "openai",
        "api_host": OPENAI_EMBEDDING_API_HOST,
    }


if __name__ == "__main__":
    sample_results = [
        {"document": "Python is a versatile programming language.", "similarity_score": 0.92},
        {"document": "Machine learning uses data to train models.", "similarity_score": 0.87},
        {"document": "Natural language processing analyzes text.", "similarity_score": 0.81},
    ]

    package = create_retrieval_brief_package(
        query="What is Python used for?",
        search_results=sample_results,
        voice="nova",
    )

    print(f"Query: {package['query']}")
    print(f"Text brief: {package['text_brief']}")
    print(f"Audio size: {len(package['audio_data'])} bytes")
    print(f"Provider: {package['provider']} ({package['api_host']})")
