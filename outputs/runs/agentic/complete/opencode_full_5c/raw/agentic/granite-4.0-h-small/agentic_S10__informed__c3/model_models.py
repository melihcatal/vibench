from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------


def build_summarize_text_request(
    text: str,
    model_provider: str = "openai",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Build a request payload for summarizing long text.

    Args:
        text: the source text to summarize.
        model_provider: identifier for the hosted model to use.
        **kwargs: provider‑specific options (e.g., temperature, max_tokens).

    Returns:
        A dict ready for the provider's SDK / REST call.
    """
    return {
        "model": model_provider,
        "messages": [
            {
                "role": "user",
                "content": f"Summarize the following text concisely:\n\n{text}",
            },
        ],
        **kwargs,
    }


def build_extract_json_request(
    text: str,
    schema: Dict[str, Any],
    model_provider: str = "openai",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Build a request payload for extracting structured JSON.

    Args:
        text: the source text.
        schema: a JSON schema describing the expected output.
        model_provider: hosted model identifier.
        **kwargs: provider‑specific options.

    Returns:
        Payload dict.
    """
    prompt = f"Extract the data below as JSON matching this schema:\n{schema}\n\nText:\n{text}"
    return {
        "model": model_provider,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        **kwargs,
    }


def build_answer_with_context_request(
    question: str,
    context: str,
    model_provider: str = "openai",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Build a request payload for answering a question using provided context.

    Args:
        question: the query.
        context: background information.
        model_provider: hosted model identifier.
        **kwargs: provider‑specific options.

    Returns:
        Payload dict.
    """
    prompt = f"You have the following context:\n\n{textwrap.indent(context, '> ')}\n\nAnswer the question concisely:\n{question}"
    return {
        "model": model_provider,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        **kwargs,
    }


def build_stream_completion_request(
    prompt: str,
    model_provider: str = "openai",
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Build a request payload for streaming token completions.

    Args:
        prompt: the prompt to complete.
        model_provider: hosted model identifier.
        **kwargs: provider‑specific options.

    Returns:
        Payload dict.
    """
    return {
        "model": model_provider,
        "messages": [{"role": "user", "content": prompt}],
        **kwargs,
    }


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def parse_summarize_text_response(response: Any) -> str:
    """Extract and clean the summary text from a provider response."""
    # Most SDKs return a string; if the response is a complex object, fall back.
    return str(response).strip() if response else ""


def parse_extract_json_response(response: Any) -> Optional[Dict[str, Any]]:
    """Attempt to load JSON from the provider output."""
    try:
        import json

        # Try common locations (some APIs embed in .choices, .content, etc.)
        if isinstance(response, dict):
            if "choices" in response and response["choices"]:
                return json.loads(response["choices"][0]["message"]["content"])
            if "content" in response:
                return json.loads(response["content"])
        return json.loads(response) if isinstance(response, str) else None
    except Exception:
        return None


def parse_answer_with_context_response(response: Any) -> str:
    """Extract the answer string from the response."""
    return str(response).strip() if response else ""


def parse_stream_completion_response(iterator: Any) -> List[str]:
    """Collect streamed token pieces into a list."""
    # Many SDKs yield tokens, others yield partial messages. Normalize.
    parts = []
    for part in iterator:
        # Assume token string or dict with token list
        txt = part.get("text", "") if isinstance(part, dict) else str(part)
        parts.append(txt.strip())
    return parts


# ---------------------------------------------------------------------------
# Normalization helpers (common interface for all providers)
# ---------------------------------------------------------------------------


def normalize_summarize_output(raw: Any) -> str:
    """Normalize any provider's summarize response to a plain string."""
    return parse_summarize_text_response(raw)


def normalize_extract_json_output(raw: Any) -> Optional[Dict[str, Any]]:
    """Normalize JSON extraction output."""
    return parse_extract_json_response(raw)


def normalize_answer_output(raw: Any) -> str:
    """Normalize answer‑with‑context responses."""
    return parse_answer_with_context_response(raw)


def normalize_stream_output(raw_iterator: Any) -> List[str]:
    """Normalize streamed token output."""
    return parse_stream_completion_response(raw_iterator)


# ---------------------------------------------------------------------------
# Utility generic request / response wrappers (optional)
# ---------------------------------------------------------------------------


def generic_request(
    provider_key: str,
    payload: Dict[str, Any],
) -> Any:
    """Route a normalized payload to the appropriate client."""
    # Pull the callable from CLIENT_MAP defined in model_client.py
    from model_client import CLIENT_MAP

    client_factory = CLIENT_MAP.get(provider_key)
    if not client_factory:
        raise ValueError(f"Unknown provider_key: {provider_key}")
    client = client_factory()
    # The SDKs generally expect a `chat.completions.create` style call.
    # Fall back to a generic `client.chat_completions.create(**payload)` if possible.
    try:
        # Try OpenAI‑style generic call first
        return client.chat_completions.create(**payload)
    except AttributeError:
        # Specific SDK call may be required; raise for now to force explicit handling
        raise NotImplementedError(
            f"Generic request not implemented for {provider_key}."
        )


def generic_response_normalizer(
    provider_key: str,
    raw: Any,
    method: str,
) -> Any:
    """Delegated normalizer based on method name."""
    method_map = {
        "summarize_text": normalize_summarize_output,
        "extract_json": normalize_extract_json_output,
        "answer_with_context": normalize_answer_output,
        "stream_completion": normalize_stream_output,
    }
    normalizer = method_map.get(method)
    if not normalizer:
        raise ValueError(f"Unknown method: {method}")
    return normalizer(raw)
