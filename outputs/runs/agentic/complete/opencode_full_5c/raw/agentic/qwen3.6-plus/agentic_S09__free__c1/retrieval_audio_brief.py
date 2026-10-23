import os
from typing import List
from embeddings_client import get_openai_client, get_embedding_model


SYSTEM_BRIEF_PROMPT = (
    "You are a helpful assistant that creates concise spoken summaries. "
    "Based on the search results provided, write a brief 2-3 sentence summary "
    "that captures the most relevant findings. Write it in a natural, conversational "
    "tone suitable for text-to-speech reading. Do not use markdown, lists, or special formatting."
)


def generate_search_brief_text(query: str, results: List[dict]) -> str:
    client = get_openai_client()

    results_context = "\n".join(
        f"Result {r.get('rank', i + 1)} (score: {r.get('score', 0):.3f}): {r['document']}"
        for i, r in enumerate(results)
    )

    user_prompt = (
        f"Search query: {query}\n\n"
        f"Top results:\n{results_context}\n\n"
        f"Please provide a concise spoken brief summarizing these results."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_BRIEF_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    brief_text = response.choices[0].message.content.strip()
    return brief_text


def generate_audio_brief(
    query: str,
    results: List[dict],
    output_path: str = "retrieval_brief.mp3",
    voice: str = "alloy",
) -> str:
    client = get_openai_client()

    brief_text = generate_search_brief_text(query, results)

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=brief_text,
        response_format="mp3",
    )

    response.stream_to_file(output_path)

    return output_path


if __name__ == "__main__":
    import json

    query = "machine learning algorithms"
    results = [
        {
            "document": "Neural networks are a key part of deep learning",
            "score": 0.89,
            "rank": 1,
        },
        {
            "document": "Support vector machines classify data points",
            "score": 0.82,
            "rank": 2,
        },
        {
            "document": "Random forests combine decision trees for prediction",
            "score": 0.78,
            "rank": 3,
        },
    ]

    brief_text = generate_search_brief_text(query, results)
    print(f"Brief text: {brief_text}")

    output_file = generate_audio_brief(
        query, results, output_path="retrieval_brief.mp3"
    )
    print(f"Audio saved to: {output_file}")
