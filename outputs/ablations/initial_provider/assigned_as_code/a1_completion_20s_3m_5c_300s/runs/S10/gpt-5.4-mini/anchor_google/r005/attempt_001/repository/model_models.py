def normalize_text_response(response):
    text = getattr(response, "text", None)
    if text is None:
        candidates = getattr(response, "candidates", None) or []
        if candidates:
            content = getattr(candidates[0], "content", None)
            parts = getattr(content, "parts", None) or []
            text = "".join(getattr(part, "text", "") or "" for part in parts)
    return {"text": text or ""}


def normalize_json_response(response):
    return {"json": getattr(response, "text", "") or ""}


def normalize_stream_chunk(chunk):
    return {"text": getattr(chunk, "text", "") or ""}


def normalize_embedding_response(response):
    embedding = getattr(response, "embedding", None)
    values = getattr(embedding, "values", None) if embedding is not None else None
    return {"embedding": list(values or [])}
