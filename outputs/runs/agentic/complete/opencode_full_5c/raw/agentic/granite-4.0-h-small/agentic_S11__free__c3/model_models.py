"""Local request, response, and normalization helpers for Managed Model Platform Workflow""

REQUEST_SCHEMA = {
    "text": str,
    "parameters": dict,
}

def normalize_request(raw):
    """Normalize incoming request payload to provider expectations."""
    # Example: ensure text key exists
    if "text" not in raw:
        raise ValueError("Request must contain a 'text' field")
    return raw

def parse_response(raw):
    """Parse raw provider response into a normalized dict."""
    # OpenAI returns {"choices": [{"text": ..., "finish_reason": ...}]},
    # simplify to {'output': ..., 'usage': ..., 'resource_id': ...}
    if isinstance(raw, list):
        # Streaming chunks
        return {"text": raw[0]["text"], "_metadata": raw[0]}
    return {
        "output": raw.get("choices", [{}])[0].get("text"),
        "usage": raw.get("usage"),
        "resource_id": raw.get("id"),
    }