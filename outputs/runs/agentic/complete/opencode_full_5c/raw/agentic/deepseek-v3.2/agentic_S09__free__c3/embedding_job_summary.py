import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from datetime import datetime


def summarize_embedding_job(
    texts: List[str],
    embeddings: List[List[float]],
    model: str = "text-embedding-3-small",
    job_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize embedding job results using OpenAI's GPT model.

    Args:
        texts: List of original texts
        embeddings: List of embedding vectors
        model: The embedding model used
        job_name: Optional name for the embedding job

    Returns:
        Dict with job summary
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Basic statistics
    num_texts = len(texts)
    num_embeddings = len(embeddings)
    embedding_dim = len(embeddings[0]) if embeddings else 0

    # Calculate average text length
    avg_text_length = sum(len(text) for text in texts) / max(num_texts, 1)

    # Create summary text for GPT analysis
    sample_texts = texts[:3] if len(texts) >= 3 else texts
    sample_preview = "\n".join(
        [
            f"- {text[:100]}..." if len(text) > 100 else f"- {text}"
            for text in sample_texts
        ]
    )

    prompt = f"""
    Analyze this embedding job and provide a concise summary:
    
    Job Details:
    - Model: {model}
    - Number of texts: {num_texts}
    - Number of embeddings: {num_embeddings}
    - Embedding dimension: {embedding_dim}
    - Average text length: {avg_text_length:.1f} characters
    
    Sample texts (first {len(sample_texts)}):
    {sample_preview}
    
    Please provide a brief analysis covering:
    1. The likely content domain based on sample texts
    2. Any potential issues (very short/long texts, duplicates, etc.)
    3. Suggested next steps for using these embeddings
    """

    # Use GPT to generate analysis
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that analyzes embedding jobs and provides concise, insightful summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    analysis = response.choices[0].message.content

    # Create comprehensive summary
    summary = {
        "job_name": job_name
        or f"embedding_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "statistics": {
            "num_texts": num_texts,
            "num_embeddings": num_embeddings,
            "embedding_dimension": embedding_dim,
            "avg_text_length": avg_text_length,
            "total_characters": sum(len(text) for text in texts),
        },
        "analysis": analysis,
        "quality_checks": {
            "texts_match_embeddings": num_texts == num_embeddings,
            "consistent_dimensions": all(
                len(emb) == embedding_dim for emb in embeddings
            ),
            "has_empty_texts": any(len(text.strip()) == 0 for text in texts),
            "has_duplicate_texts": len(set(texts)) < len(texts),
        },
        "recommendations": [
            "Store embeddings with metadata for future retrieval",
            "Consider normalizing embeddings for cosine similarity",
            "Monitor token usage for cost optimization",
        ],
    }

    return summary
