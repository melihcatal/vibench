import os
from openai import OpenAI
from typing import List, Dict, Any
import numpy as np


def moderation_reason_embedding(moderation_reasons: List[str]) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval using OpenAI's embeddings API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Generate embeddings for each moderation reason
    embeddings = []
    for reason in moderation_reasons:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=reason
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)

    # Convert to numpy array for similarity calculations
    embedding_array = np.array(embeddings)

    # Calculate centroid (average embedding)
    centroid = np.mean(embedding_array, axis=0)

    # Calculate pairwise similarities
    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            # Cosine similarity
            dot_product = np.dot(embeddings[i], embeddings[j])
            norm_i = np.linalg.norm(embeddings[i])
            norm_j = np.linalg.norm(embeddings[j])
            similarity = (
                dot_product / (norm_i * norm_j) if norm_i > 0 and norm_j > 0 else 0
            )
            similarities.append(
                {
                    "reason_1_index": i,
                    "reason_2_index": j,
                    "similarity": float(similarity),
                }
            )

    # Sort similarities
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Use GPT-4 to cluster similar reasons
    cluster_prompt = f"""Analyze these moderation reasons and identify common themes or clusters:

{chr(10).join([f"{i + 1}. {reason}" for i, reason in enumerate(moderation_reasons)])}

Return a JSON object with:
- "clusters": list of clusters, each with "theme", "reason_indices", "example_reason"
- "common_themes": list of most frequent themes
- "recommended_tags": list of tags for categorization
"""

    cluster_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation analyst. Identify themes in moderation reasons.",
            },
            {"role": "user", "content": cluster_prompt},
        ],
        response_format={"type": "json_object"},
    )

    clusters = eval(cluster_response.choices[0].message.content)

    return {
        "total_reasons": len(moderation_reasons),
        "embeddings_generated": len(embeddings),
        "embedding_model": "text-embedding-3-small",
        "centroid_embedding": centroid.tolist(),
        "pairwise_similarities": similarities[:10],  # Top 10 most similar pairs
        "average_similarity": float(np.mean([s["similarity"] for s in similarities]))
        if similarities
        else 0,
        "clusters": clusters,
        "embedding_dimensions": len(centroid),
    }
