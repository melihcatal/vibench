import os
from typing import List, Dict, Any
import openai


def embed_secret_audit_notes(audit_notes: List[str]) -> Dict[str, Any]:
    """
    Embed secret audit notes for semantic search using OpenAI Embeddings API.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Prepare text for embedding
    texts_to_embed = []
    for i, note in enumerate(audit_notes):
        if note and isinstance(note, str) and note.strip():
            texts_to_embed.append(
                {"id": f"audit_note_{i}", "text": note.strip(), "original_index": i}
            )

    if not texts_to_embed:
        return {
            "embeddings": [],
            "model_used": "text-embedding-3-small",
            "total_notes": 0,
            "error": "No valid audit notes provided",
        }

    try:
        # Call OpenAI Embeddings API
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[item["text"] for item in texts_to_embed],
            encoding_format="float",
        )

        embeddings = []
        for i, embedding_data in enumerate(response.data):
            note_info = texts_to_embed[i]
            embeddings.append(
                {
                    "id": note_info["id"],
                    "original_index": note_info["original_index"],
                    "text_preview": note_info["text"][:100] + "..."
                    if len(note_info["text"]) > 100
                    else note_info["text"],
                    "embedding": embedding_data.embedding,
                    "embedding_length": len(embedding_data.embedding),
                    "token_count": embedding_data.embedding,  # Note: actual token count would be from usage
                }
            )

        # Calculate some statistics
        embedding_dimensions = len(response.data[0].embedding) if response.data else 0

        return {
            "embeddings": embeddings,
            "model_used": "text-embedding-3-small",
            "total_notes": len(audit_notes),
            "valid_notes_embedded": len(texts_to_embed),
            "embedding_dimensions": embedding_dimensions,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens
                if hasattr(response, "usage")
                else None,
                "total_tokens": response.usage.total_tokens
                if hasattr(response, "usage")
                else None,
            },
        }

    except openai.APIConnectionError as e:
        raise Exception(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        raise Exception(f"OpenAI API rate limit exceeded: {e}")
    except openai.APIStatusError as e:
        raise Exception(f"OpenAI API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during embedding: {e}")


def search_similar_audit_notes(
    query: str, embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar audit notes using cosine similarity.
    Requires the query to be embedded first.
    """
    if not embeddings:
        return []

    # Embed the query
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        query_response = client.embeddings.create(
            model="text-embedding-3-small", input=[query], encoding_format="float"
        )

        query_embedding = query_response.data[0].embedding

        # Calculate cosine similarities
        import numpy as np

        similarities = []
        for emb_data in embeddings:
            if "embedding" not in emb_data:
                continue

            doc_embedding = emb_data["embedding"]

            # Convert to numpy arrays for calculation
            query_vec = np.array(query_embedding)
            doc_vec = np.array(doc_embedding)

            # Cosine similarity
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )

            similarities.append(
                {
                    "id": emb_data["id"],
                    "original_index": emb_data["original_index"],
                    "text_preview": emb_data["text_preview"],
                    "similarity": float(similarity),
                    "embedding_data": emb_data,
                }
            )

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        return similarities[:top_k]

    except Exception as e:
        raise Exception(f"Error searching similar notes: {e}")
