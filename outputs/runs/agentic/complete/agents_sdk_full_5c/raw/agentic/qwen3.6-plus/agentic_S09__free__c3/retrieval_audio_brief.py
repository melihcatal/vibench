"""
Generate a spoken brief from retrieved search results.

Provider: OpenAI Chat Completions API (GPT-4o mini for summarization)
Provider SDK: openai
Provider TTS: OpenAI Text-to-Speech API
Provider TTS Model: tts-1
Provider Env: OPENAI_API_KEY
Provider Host: api.openai.com
"""

import os
from typing import Optional

from openai import OpenAI

from embeddings_models import SearchResult


def generate_retrieval_audio_brief(
    results: list[SearchResult],
    query: str,
    output_path: Optional[str] = None,
    tts_model: str = "tts-1",
    voice: str = "alloy",
) -> str:
    """Generate a spoken audio brief summarizing retrieved search results.

    Uses GPT-4o mini to create a concise summary, then converts it to speech
    via the OpenAI TTS API (model: tts-1).

    Args:
        results: Ranked list of SearchResult from semantic search.
        query: The original search query.
        output_path: File path for the audio output (default: retrieval_brief.mp3).
        tts_model: OpenAI TTS model (default: tts-1).
        voice: OpenAI TTS voice name (default: alloy).

    Returns:
        Path to the generated audio file.
    """
    if not results:
        raise ValueError("No search results provided to generate a brief from.")

    # Step 1: Create a concise spoken summary using GPT-4o mini via api.openai.com
    chat_client = OpenAI()

    result_text_blocks = []
    for i, r in enumerate(results):
        result_text_blocks.append(f"Result {i + 1} (score {r.score:.3f}): {r.document}")

    combined_results = "\n".join(result_text_blocks)

    system_prompt = (
        "You are a research assistant. Write a short spoken summary (2-4 sentences) "
        "that synthesizes the search results for the given query. "
        "Write in a natural spoken style suitable for text-to-speech. "
        "Do not include scores or URLs. Just the summary text."
    )

    summary_response = chat_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}\n\nResults:\n{combined_results}"},
        ],
        temperature=0.3,
        max_tokens=256,
    )
    summary_text = summary_response.choices[0].message.content.strip()

    # Step 2: Convert summary to speech using OpenAI TTS (tts-1 model)
    audio_path = output_path or os.path.join(os.getcwd(), "retrieval_brief.mp3")
    speech_response = chat_client.audio.speech.create(
        model=tts_model,
        voice=voice,
        input=summary_text,
    )
    with open(audio_path, "wb") as f:
        f.write(speech_response.content)

    return audio_path


if __name__ == "__main__":
    from embeddings_models import SearchResult

    sample_results = [
        SearchResult(
            document="Neural networks are trained using backpropagation and gradient descent.",
            score=0.892,
            index=0,
        ),
        SearchResult(
            document="Deep learning requires large datasets and GPU acceleration.",
            score=0.845,
            index=1,
        ),
        SearchResult(
            document="Convolutional neural networks excel at image recognition tasks.",
            score=0.781,
            index=2,
        ),
    ]

    audio_file = generate_retrieval_audio_brief(
        results=sample_results,
        query="How do I train a neural network?",
    )
    print(f"Audio brief generated at: {audio_file}")
