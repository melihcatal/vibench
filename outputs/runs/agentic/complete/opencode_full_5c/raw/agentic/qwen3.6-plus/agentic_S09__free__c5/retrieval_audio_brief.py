from typing import List, Dict
import os
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import SearchResult


def generate_audio_brief_script(
    results: List[SearchResult], max_results: int = 5
) -> str:
    top_results = results[:max_results]
    script_parts = []
    script_parts.append(
        f'Here are the top {len(top_results)} results for your query: "{top_results[0].query}"'
    )
    for i, result in enumerate(top_results, 1):
        doc_preview = result.document[:200]
        script_parts.append(f"Result {i}: {doc_preview}")
    script_parts.append("End of results.")
    return "\n".join(script_parts)


def generate_spoken_brief(
    results: List[SearchResult],
    max_results: int = 5,
    voice: str = "alloy",
    output_path: str = "retrieval_brief.mp3",
) -> str:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    script = generate_audio_brief_script(results, max_results)
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=script,
        response_format="mp3",
    )
    response.stream_to_file(output_path)
    return output_path


def generate_brief_text(results: List[SearchResult], max_results: int = 5) -> str:
    top_results = results[:max_results]
    lines = []
    lines.append(f'Search Brief for: "{top_results[0].query}"')
    lines.append("=" * 50)
    for i, result in enumerate(top_results, 1):
        lines.append(f"\n[{i}] Score: {result.score:.4f}")
        lines.append(f"    {result.document}")
    lines.append(f"\nTotal results shown: {len(top_results)}")
    return "\n".join(lines)


def generate_audio_brief_from_texts(
    query: str,
    documents: List[str],
    scores: List[float],
    max_results: int = 5,
    voice: str = "alloy",
    output_path: str = "retrieval_brief.mp3",
) -> str:
    results = []
    for doc, score in zip(documents, scores):
        results.append(
            SearchResult(
                query=query,
                document=doc,
                score=score,
                rank=0,
                embedding=[],
            )
        )
    results.sort(key=lambda r: r.score, reverse=True)
    for rank, result in enumerate(results, 1):
        result.rank = rank
    return generate_spoken_brief(results, max_results, voice, output_path)


def create_summary_for_tts(results: List[SearchResult], max_results: int = 3) -> str:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    top_results = results[:max_results]
    context = "\n".join([f"- {r.document}" for r in top_results])
    prompt = (
        f"Create a concise spoken summary (2-3 sentences) based on these search results "
        f"for the query '{top_results[0].query}'. "
        f"Make it natural and conversational for text-to-speech.\n\n"
        f"Results:\n{context}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You create clear, concise spoken summaries for text-to-speech output.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )
    summary = response.choices[0].message.content.strip()
    return summary


if __name__ == "__main__":
    sample_results = [
        SearchResult(
            query="What is AI?",
            document="Artificial intelligence is the simulation of human intelligence by machines",
            score=0.92,
            rank=1,
        ),
        SearchResult(
            query="What is AI?",
            document="Machine learning enables systems to learn from data automatically",
            score=0.85,
            rank=2,
        ),
        SearchResult(
            query="What is AI?",
            document="Deep learning uses neural networks with multiple layers",
            score=0.78,
            rank=3,
        ),
    ]
    brief_text = generate_brief_text(sample_results)
    print(brief_text)
