import os
import openai
from typing import List, Dict, Any


def transcript_embedding(transcript_text):
    """Embed transcript segments for semantic retrieval using OpenAI embeddings."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=transcript_text,
            encoding_format="float",
        )

        embedding = response.data[0].embedding

        return {
            "text": transcript_text,
            "embedding": embedding,
            "dimensions": len(embedding),
            "model": "text-embedding-3-small",
            "provider": "OpenAI",
        }

    except openai.OpenAIError as e:
        return {"error": str(e), "provider": "OpenAI"}


def embed_segments(segments: List[Dict[str, Any]], batch_size=10):
    """Embed multiple transcript segments."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    embedded_segments = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i : i + batch_size]

        texts = []
        for segment in batch:
            if isinstance(segment, dict):
                text = segment.get("text", "")
            else:
                text = str(segment)
            texts.append(text)

        try:
            response = client.embeddings.create(
                model="text-embedding-3-small", input=texts, encoding_format="float"
            )

            for j, embedding_data in enumerate(response.data):
                segment_index = i + j
                if segment_index < len(segments):
                    segment = segments[segment_index]

                    embedded_segment = {
                        "segment_index": segment_index,
                        "embedding": embedding_data.embedding,
                        "dimensions": len(embedding_data.embedding),
                        "model": "text-embedding-3-small",
                        "provider": "OpenAI",
                    }

                    if isinstance(segment, dict):
                        embedded_segment.update(
                            {
                                "text": segment.get("text", ""),
                                "metadata": {
                                    k: v for k, v in segment.items() if k != "text"
                                },
                            }
                        )
                    else:
                        embedded_segment["text"] = str(segment)

                    embedded_segments.append(embedded_segment)

        except openai.OpenAIError as e:
            for j in range(len(batch)):
                segment_index = i + j
                if segment_index < len(segments):
                    embedded_segments.append(
                        {
                            "segment_index": segment_index,
                            "error": str(e),
                            "provider": "OpenAI",
                        }
                    )

    return {
        "embedded_segments": embedded_segments,
        "total_segments": len(segments),
        "successful_embeddings": len(
            [s for s in embedded_segments if "embedding" in s]
        ),
        "model": "text-embedding-3-small",
        "provider": "OpenAI",
    }


def semantic_search(query: str, embeddings: List[Dict[str, Any]], top_k=5):
    """Perform semantic search on embedded transcript segments."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    # Embed the query
    try:
        query_response = client.embeddings.create(
            model="text-embedding-3-small", input=query, encoding_format="float"
        )

        query_embedding = query_response.data[0].embedding

        # Calculate cosine similarity (simplified)
        import numpy as np

        results = []
        for emb_data in embeddings:
            if "embedding" not in emb_data:
                continue

            segment_embedding = np.array(emb_data["embedding"])
            query_vec = np.array(query_embedding)

            # Cosine similarity
            similarity = np.dot(query_vec, segment_embedding) / (
                np.linalg.norm(query_vec) * np.linalg.norm(segment_embedding)
            )

            results.append(
                {
                    "segment_index": emb_data.get("segment_index"),
                    "text": emb_data.get("text", ""),
                    "similarity": float(similarity),
                    "metadata": emb_data.get("metadata", {}),
                }
            )

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)

        return {
            "query": query,
            "results": results[:top_k],
            "model": "text-embedding-3-small",
            "provider": "OpenAI",
        }

    except (openai.OpenAIError, ValueError) as e:
        return {"error": str(e), "provider": "OpenAI"}
