"""
Summarize embedding job results using OpenAI GPT-4o.

After running an embedding job, this module uses OpenAI's chat completions
API with model gpt-4o to generate a human-readable summary of the results,
including statistics about the corpus, embedding quality indicators, and
recommendations.

Requires OPENAI_API_KEY environment variable or explicit api_key parameter.
"""

import json
from typing import List, Optional

from openai import OpenAI

from embeddings_client import get_openai_client

OPENAI_CHAT_MODEL = "gpt-4o"


def summarize_embedding_job(
    job_metadata: dict,
    embedding_stats: dict,
    sample_texts: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    model: str = OPENAI_CHAT_MODEL,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Generate a summary of an embedding job using OpenAI GPT-4o.

    Args:
        job_metadata: Dict with job details (model, dimensions, count, timestamp, etc.).
        embedding_stats: Dict with statistics (avg_norm, min_norm, token_usage, etc.).
        sample_texts: Optional sample input texts for context.
        api_key: OpenAI API key.
        model: OpenAI chat model identifier, default gpt-4o.
        client: Pre-configured OpenAI client (optional).

    Returns:
        Human-readable summary string.
    """
    if client is None:
        client = get_openai_client(api_key)

    system_prompt = (
        "You are an AI assistant that summarizes embedding job results. "
        "Provide a concise, professional summary with key statistics, "
        "quality observations, and any recommendations for improving "
        "future embedding runs. Format the output as plain text with clear sections."
    )

    user_content_parts = [
        f"Embedding job metadata:\n{json.dumps(job_metadata, indent=2)}",
        f"Embedding statistics:\n{json.dumps(embedding_stats, indent=2)}",
    ]
    if sample_texts:
        user_content_parts.append(
            f"Sample texts embedded ({len(sample_texts)} shown):\n"
            + "\n".join(f"- {t[:120]}..." if len(t) > 120 else f"- {t}" for t in sample_texts)
        )

    user_content = "\n\n".join(user_content_parts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    summary = response.choices[0].message.content
    return summary


def generate_job_report(
    total_documents: int,
    total_tokens: int,
    model_used: str,
    dimensions: int,
    avg_similarity: Optional[float] = None,
    sample_texts: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Convenience wrapper to generate a report from basic job parameters.

    Args:
        total_documents: Number of documents embedded.
        total_tokens: Total token consumption.
        model_used: Embedding model identifier.
        dimensions: Output vector dimensions.
        avg_similarity: Average pairwise similarity (optional).
        sample_texts: Sample input texts.
        api_key: OpenAI API key.
        client: Optional pre-built OpenAI client.

    Returns:
        Generated summary report.
    """
    job_metadata = {
        "total_documents": total_documents,
        "model_used": model_used,
        "dimensions": dimensions,
        "total_tokens": total_tokens,
    }
    embedding_stats = {
        "total_tokens": total_tokens,
        "avg_tokens_per_doc": round(total_tokens / max(total_documents, 1), 2),
    }
    if avg_similarity is not None:
        embedding_stats["avg_pairwise_similarity"] = avg_similarity

    return summarize_embedding_job(
        job_metadata=job_metadata,
        embedding_stats=embedding_stats,
        sample_texts=sample_texts,
        api_key=api_key,
        client=client,
    )
