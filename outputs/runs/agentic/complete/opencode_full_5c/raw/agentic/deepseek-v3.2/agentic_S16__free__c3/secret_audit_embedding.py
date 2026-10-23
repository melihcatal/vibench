import os
import json
from typing import List, Dict, Any
import openai


def secret_audit_embedding(
    audit_notes: List[Dict[str, Any]], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed secret audit notes for semantic search using OpenAI embeddings.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=api_key)

    try:
        texts_to_embed = []
        note_metadata = []

        for i, note in enumerate(audit_notes):
            secret_name = note.get("secret_name", f"secret_{i}")
            note_text = note.get("note", "")
            author = note.get("author", "unknown")
            timestamp = note.get("timestamp", "")
            labels = note.get("labels", [])

            if not note_text.strip():
                continue

            combined_text = f"Secret: {secret_name}. Note: {note_text}. Author: {author}. Labels: {', '.join(labels)}"

            texts_to_embed.append(combined_text)
            note_metadata.append(
                {
                    "index": i,
                    "secret_name": secret_name,
                    "note_preview": note_text[:100] + "..."
                    if len(note_text) > 100
                    else note_text,
                    "author": author,
                    "timestamp": timestamp,
                    "labels": labels,
                    "original_note": note_text,
                }
            )

        if not texts_to_embed:
            return {
                "provider": "openai",
                "model": model,
                "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
                "embeddings": [],
                "metadata": [],
                "stats": {
                    "total_notes": 0,
                    "embedded_notes": 0,
                    "embedding_dimensions": 0,
                },
            }

        response = client.embeddings.create(
            model=model, input=texts_to_embed, encoding_format="float"
        )

        embeddings = []
        for i, embedding_data in enumerate(response.data):
            embeddings.append(
                {
                    "index": i,
                    "embedding": embedding_data.embedding,
                    "text_preview": texts_to_embed[i][:200] + "..."
                    if len(texts_to_embed[i]) > 200
                    else texts_to_embed[i],
                    "metadata_index": i,
                }
            )

        stats = {
            "total_notes": len(audit_notes),
            "embedded_notes": len(texts_to_embed),
            "embedding_dimensions": len(response.data[0].embedding)
            if response.data
            else 0,
            "model": model,
            "total_tokens": response.usage.total_tokens
            if hasattr(response, "usage")
            else 0,
        }

        result = {
            "provider": "openai",
            "model": model,
            "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
            "embeddings": embeddings,
            "metadata": note_metadata,
            "stats": stats,
        }

        semantic_clusters = []
        if len(embeddings) >= 3:
            try:
                from sklearn.cluster import KMeans
                import numpy as np

                embedding_vectors = np.array([e["embedding"] for e in embeddings])
                n_clusters = min(5, len(embeddings))

                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(embedding_vectors)

                for cluster_id in range(n_clusters):
                    cluster_indices = [
                        i
                        for i, label in enumerate(cluster_labels)
                        if label == cluster_id
                    ]
                    cluster_notes = [note_metadata[i] for i in cluster_indices]

                    cluster_secrets = list(
                        set([note["secret_name"] for note in cluster_notes])
                    )
                    cluster_authors = list(
                        set([note["author"] for note in cluster_notes])
                    )

                    cluster_keywords = []
                    all_notes = " ".join(
                        [note["original_note"] for note in cluster_notes]
                    )
                    words = all_notes.lower().split()
                    from collections import Counter

                    common_words = Counter(words).most_common(5)
                    cluster_keywords = [
                        word for word, count in common_words if len(word) > 3
                    ]

                    semantic_clusters.append(
                        {
                            "cluster_id": cluster_id,
                            "size": len(cluster_indices),
                            "secrets": cluster_secrets[:5],
                            "authors": cluster_authors[:3],
                            "keywords": cluster_keywords,
                            "centroid": kmeans.cluster_centers_[cluster_id].tolist(),
                        }
                    )

                result["semantic_clusters"] = semantic_clusters
                result["stats"]["clusters_created"] = n_clusters

            except ImportError:
                result["semantic_clusters"] = "skipped (scikit-learn not available)"
            except Exception as e:
                result["semantic_clusters"] = f"error: {str(e)}"

        return result

    except openai.AuthenticationError:
        raise PermissionError("Invalid OpenAI API key") from None
    except openai.RateLimitError:
        raise RuntimeError("OpenAI rate limit exceeded") from None
    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error creating embeddings: {e}") from e
