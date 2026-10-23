import os
from typing import List, Dict, Any
import numpy as np
import cohere


def embed_log_messages(
    log_messages: List[str], model: str = "embed-english-v3.0"
) -> Dict[str, Any]:
    """Embed selected log messages for semantic retrieval using Cohere Embed API."""

    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError(
            "Cohere API key must be set in COHERE_API_KEY environment variable"
        )

    client = cohere.Client(api_key)

    valid_messages = [msg for msg in log_messages if msg and isinstance(msg, str)]

    if not valid_messages:
        return {
            "total_messages": len(log_messages),
            "embeddings": [],
            "errors": ["No valid messages to embed"],
        }

    try:
        response = client.embed(
            texts=valid_messages, model=model, input_type="search_document"
        )

        embeddings = []
        for i, embedding in enumerate(response.embeddings):
            embeddings.append(
                {
                    "message": valid_messages[i],
                    "embedding": embedding,
                    "embedding_dimensions": len(embedding),
                    "model": model,
                }
            )

        return {
            "total_messages": len(log_messages),
            "valid_messages": len(valid_messages),
            "embeddings": embeddings,
            "model": model,
            "provider": "Cohere",
        }

    except Exception as e:
        return {
            "total_messages": len(log_messages),
            "embeddings": [],
            "errors": [f"Cohere API error: {str(e)}"],
            "model": model,
        }


def embed_log_entries(
    log_entries: List[Dict[str, Any]],
    text_field: str = "message",
    model: str = "embed-english-v3.0",
) -> Dict[str, Any]:
    """Embed log entries and attach embeddings to them."""

    messages = []
    entry_map = []

    for i, entry in enumerate(log_entries):
        if (
            text_field in entry
            and isinstance(entry[text_field], str)
            and entry[text_field].strip()
        ):
            messages.append(entry[text_field])
            entry_map.append(i)

    embedding_result = embed_log_messages(messages, model)

    embedded_entries = []

    for i, entry in enumerate(log_entries):
        embedded_entry = entry.copy()

        if i in entry_map:
            map_index = entry_map.index(i)
            if map_index < len(embedding_result["embeddings"]):
                embedding_data = embedding_result["embeddings"][map_index]
                embedded_entry["embedding"] = embedding_data["embedding"]
                embedded_entry["embedding_model"] = model
                embedded_entry["embedding_provider"] = "Cohere"

        embedded_entries.append(embedded_entry)

    return {
        "original_entries": log_entries,
        "embedded_entries": embedded_entries,
        "embedding_summary": {
            "total_entries": len(log_entries),
            "embedded_entries": len([e for e in embedded_entries if "embedding" in e]),
            "model": model,
            "embedding_dimensions": embedding_result["embeddings"][0][
                "embedding_dimensions"
            ]
            if embedding_result["embeddings"]
            else 0,
            "provider": "Cohere",
        },
    }


def find_similar_logs(
    query: str, embedded_logs: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """Find logs similar to a query using cosine similarity."""

    if not embedded_logs or not any("embedding" in log for log in embedded_logs):
        return []

    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError(
            "Cohere API key must be set in COHERE_API_KEY environment variable"
        )

    client = cohere.Client(api_key)

    try:
        query_response = client.embed(
            texts=[query], model="embed-english-v3.0", input_type="search_query"
        )

        if not query_response.embeddings:
            return []

        query_embedding = np.array(query_response.embeddings[0])

        similarities = []

        for i, log in enumerate(embedded_logs):
            if "embedding" in log:
                log_embedding = np.array(log["embedding"])

                similarity = np.dot(query_embedding, log_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(log_embedding)
                )

                similarities.append(
                    {"index": i, "similarity": float(similarity), "log_entry": log}
                )

        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        return similarities[:top_k]

    except Exception as e:
        print(f"Error finding similar logs: {str(e)}")
        return []


if __name__ == "__main__":
    test_logs = [
        {
            "message": "Database connection timeout error",
            "severity": "ERROR",
            "component": "database",
        },
        {
            "message": "User authentication failed - invalid credentials",
            "severity": "WARNING",
            "component": "auth",
        },
        {
            "message": "API request rate limit exceeded",
            "severity": "ERROR",
            "component": "api",
        },
        {
            "message": "File upload completed successfully",
            "severity": "INFO",
            "component": "storage",
        },
    ]

    embedded_result = embed_log_entries(test_logs)

    print(
        f"Embedded {embedded_result['embedding_summary']['embedded_entries']} log entries"
    )
    print(f"Using model: {embedded_result['embedding_summary']['model']}")
    print(f"Provider: {embedded_result['embedding_summary']['provider']}")

    query = "database connection problems"
    similar_logs = find_similar_logs(
        query, embedded_result["embedded_entries"], top_k=2
    )

    print(f"\nLogs similar to '{query}':")
    for i, similar in enumerate(similar_logs):
        print(f"{i + 1}. Similarity: {similar['similarity']:.3f}")
        print(f"   Message: {similar['log_entry']['message']}")
        print(f"   Severity: {similar['log_entry']['severity']}")
