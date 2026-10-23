"""Summarize embedding job results using OpenAI GPT-4o-mini chat completions.

Uses OpenAI's GPT-4o-mini model to generate a summary of embedding job outputs,
including statistics, notable patterns, and document cluster themes.
"""

import os
import json
from typing import List, Dict, Any

from openai import OpenAI


OPENAI_CHAT_MODEL = "gpt-4o-mini"


def get_openai_client() -> OpenAI:
    """Create an OpenAI client from environment configuration."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def summarize_embedding_job(
    job_results: List[Dict[str, Any]],
    job_metadata: Dict[str, Any] = None,
    model: str = None,
) -> str:
    """Generate a natural-language summary of embedding job results using GPT-4o-mini.

    Args:
        job_results: List of embedding result dicts, each containing 'text',
                     'embedding', 'token_count', and optionally 'similarity_score'.
        job_metadata: Optional job-level metadata (model used, batch size, duration).
        model: OpenAI chat model ID (defaults to gpt-4o-mini).

    Returns:
        Summary text describing the embedding job results.
    """
    client = get_openai_client()
    model_id = model or OPENAI_CHAT_MODEL

    results_summary = json.dumps({
        "num_documents": len(job_results),
        "avg_tokens": sum(r.get("token_count", 0) for r in job_results) / max(len(job_results), 1),
        "top_texts": [
            {"text": r.get("text", "")[:120], "tokens": r.get("token_count", 0)}
            for r in job_results[:10]
        ],
        "metadata": job_metadata or {},
    }, ensure_ascii=False)

    system_prompt = (
        "You are an embedding analytics assistant. Summarize the embedding job results. "
        "Provide key statistics, notable patterns in the embedded texts, and any "
        "observed clustering themes. Keep the summary concise (3-5 sentences)."
    )

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Embedding job results:\n{results_summary}"},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content


def summarize_with_similarity_insights(
    job_results: List[Dict[str, Any]],
    query: str = None,
    model: str = None,
) -> str:
    """Summarize embedding job results with query-similarity insights via GPT-4o-mini.

    Args:
        job_results: List of embedding results with optional similarity scores.
        query: The original search query used for similarity scoring.
        model: OpenAI chat model ID.

    Returns:
        Summary text highlighting similarity insights.
    """
    client = get_openai_client()
    model_id = model or OPENAI_CHAT_MODEL

    scored_texts = []
    for r in job_results:
        scored_texts.append({
            "text": r.get("text", "")[:150],
            "similarity": r.get("similarity_score"),
        })

    insights_summary = json.dumps({
        "query": query,
        "results": scored_texts,
        "highest_similarity": max((r.get("similarity_score", 0) for r in job_results), default=0),
        "lowest_similarity": min((r.get("similarity_score", 0) for r in job_results), default=0),
    }, ensure_ascii=False)

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a search analytics assistant. Analyze the embedding-based "
                    "search results and summarize what the query found, which documents "
                    "were most relevant, and any patterns in relevance scores."
                ),
            },
            {"role": "user", "content": f"Search results:\n{insights_summary}"},
        ],
        temperature=0.3,
        max_tokens=600,
    )

    return response.choices[0].message.content


def main():
    sample_results = [
        {"text": "Deep learning models use neural networks with many layers.", "token_count": 10, "similarity_score": 0.87},
        {"text": "Python is a popular programming language for data science.", "token_count": 11, "similarity_score": 0.42},
        {"text": "Transfer learning applies pre-trained models to new domains.", "token_count": 10, "similarity_score": 0.79},
    ]
    query = "neural network architectures"

    summary = summarize_with_similarity_insights(sample_results, query=query)
    print(f"Job Summary (gpt-4o-mini):\n{summary}")


if __name__ == "__main__":
    main()
