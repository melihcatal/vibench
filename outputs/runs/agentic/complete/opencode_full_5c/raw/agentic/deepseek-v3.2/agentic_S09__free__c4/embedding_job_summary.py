import os
from typing import List, Dict, Any
from openai import OpenAI
import numpy as np


def embedding_job_summary(
    embeddings: List[List[float]],
    texts: List[str],
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """
    Summarize embedding job results using OpenAI's API for analysis.

    Args:
        embeddings: List of embedding vectors
        texts: List of original texts
        model: The embedding model used

    Returns:
        Dictionary with job summary statistics and analysis
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Calculate basic statistics
    dimensions = len(embeddings[0]) if embeddings else 0
    embedding_array = np.array(embeddings)

    # Compute statistics
    mean_vector = np.mean(embedding_array, axis=0).tolist()
    std_vector = np.std(embedding_array, axis=0).tolist()

    # Compute pairwise similarities
    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            vec1 = np.array(embeddings[i])
            vec2 = np.array(embeddings[j])
            similarity = np.dot(vec1, vec2) / (
                np.linalg.norm(vec1) * np.linalg.norm(vec2)
            )
            similarities.append(float(similarity))

    # Generate analysis using OpenAI
    text_samples = texts[:3] if len(texts) > 3 else texts
    sample_text = "\n".join(
        [f"Sample {i + 1}: {text[:100]}..." for i, text in enumerate(text_samples)]
    )

    prompt = f"""
    Analyze these embedding job results:
    - Model: {model}
    - Number of texts: {len(texts)}
    - Embedding dimensions: {dimensions}
    - Text samples: {sample_text}
    
    Provide a brief analysis of the embedding quality and any observations about the text corpus.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that analyzes embedding job results.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )
        analysis = response.choices[0].message.content
    except Exception as e:
        analysis = f"Analysis generation failed: {str(e)}"

    summary = {
        "model": model,
        "num_texts": len(texts),
        "dimensions": dimensions,
        "statistics": {
            "mean_vector_length": len(mean_vector),
            "std_vector_length": len(std_vector),
            "similarity_stats": {
                "mean": float(np.mean(similarities)) if similarities else 0.0,
                "std": float(np.std(similarities)) if similarities else 0.0,
                "min": float(min(similarities)) if similarities else 0.0,
                "max": float(max(similarities)) if similarities else 0.0,
            },
        },
        "analysis": analysis,
        "metadata": {"provider": "openai", "model_family": "text-embedding-3"},
    }

    return summary
