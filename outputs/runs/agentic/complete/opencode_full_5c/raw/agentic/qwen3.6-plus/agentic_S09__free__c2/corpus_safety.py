import re
from embeddings_client import create_embeddings_client, handle_embedding_error
from embeddings_models import EmbeddingRequest, EmbeddingResponse

DEFAULT_MAX_LENGTH = 8192
DEFAULT_SENSITIVE_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{16}\b"),
    re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    re.compile(
        r"\b(?:password|secret|token|api_key|apikey)\s*[:=]\s*\S+", re.IGNORECASE
    ),
]


def check_corpus_text(
    texts, model=None, client=None, api_key=None, max_length=None, check_sensitive=True
):
    if not texts:
        raise ValueError("texts list must not be empty")

    if client is None:
        client, model = create_embeddings_client(model=model, api_key=api_key)

    if model is None:
        model = "text-embedding-3-small"

    limit = max_length or DEFAULT_MAX_LENGTH
    results = []

    for idx, text in enumerate(texts):
        issues = []

        if not text or not text.strip():
            issues.append("empty_text")

        if text and len(text) > limit:
            issues.append("exceeds_max_length")

        if check_sensitive and text:
            for pattern in DEFAULT_SENSITIVE_PATTERNS:
                if pattern.search(text):
                    issues.append("contains_sensitive_data")
                    break

        is_safe = len(issues) == 0

        results.append(
            {
                "index": idx,
                "text_length": len(text) if text else 0,
                "is_safe": is_safe,
                "issues": issues,
            }
        )

    safe_texts = []
    unsafe_texts = []
    for i, res in enumerate(results):
        if res["is_safe"]:
            safe_texts.append(texts[i])
        else:
            unsafe_texts.append({"index": i, "text": texts[i], "issues": res["issues"]})

    if safe_texts:
        request = EmbeddingRequest(
            texts=safe_texts,
            model=model,
        )
        try:
            response = client.embeddings.create(**request.to_payload())
            result = EmbeddingResponse.from_openai_response(response)
            for safe_entry, emb in zip(
                [r for r in results if r["is_safe"]], result.embeddings
            ):
                safe_entry["embedding"] = emb
        except Exception as exc:
            handle_embedding_error(exc)

    return {
        "model": model,
        "total_checked": len(texts),
        "safe_count": len(safe_texts),
        "unsafe_count": len(unsafe_texts),
        "results": results,
        "unsafe_details": unsafe_texts,
    }
