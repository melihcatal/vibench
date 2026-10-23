from sentence_transformers import SentenceTransformer
from fetch_recent_logs import fetch_recent_logs


def embed_log_messages(field_filters: dict, hours: int = 1) -> Dict[str, Any]:
    """
    Embeds selected log messages for semantic retrieval using Sentence Transformers.

    Args:
        field_filters: Dictionary of field-value pairs to filter logs.
        hours: Time range in hours to query logs from.

    Returns:
        Dictionary containing log messages and their embeddings.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logs = fetch_recent_logs(field_filters, hours=hours)

    if not logs:
        return {"summary": "No logs found for the specified filters."}

    messages = [log.get("message", "") for log in logs]
    embeddings = model.encode(messages, convert_to_tensor=True)

    results = []
    for message, embedding in zip(messages, embeddings):
        results.append({"message": message, "embedding": embedding.tolist()})

    return {
        "total_logs_embedded": len(results),
        "embedding_model": "all-MiniLM-L6-v2",
        "results": results,
    }
