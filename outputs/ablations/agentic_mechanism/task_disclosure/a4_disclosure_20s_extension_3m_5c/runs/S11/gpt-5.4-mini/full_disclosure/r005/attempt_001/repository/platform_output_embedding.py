import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

try:
    from openai import OpenAI
except Exception as exc:  # pragma: no cover
    OpenAI = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    if isinstance(value, dict):
        for key in ("text", "output", "content", "message", "result"):
            if key in value:
                return _coerce_text(value[key])
        return " ".join(f"{k}:{_coerce_text(v)}" for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_coerce_text(item) for item in value)
    return str(value)


def normalize_platform_output(output: Any) -> str:
    return _coerce_text(output).strip()


def get_openai_client(api_key: Optional[str] = None) -> Any:
    if OpenAI is None:
        raise ImportError("openai package is required") from _IMPORT_ERROR
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def embed_platform_output(
    output: Any,
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    client: Any = None,
) -> Dict[str, Any]:
    text = normalize_platform_output(output)
    if client is None:
        client = get_openai_client(api_key=api_key)
    response = client.embeddings.create(model=model, input=text)
    embedding = response.data[0].embedding if response.data else []
    return {
        "provider": "openai",
        "model": model,
        "input_text": text,
        "embedding": embedding,
        "usage": getattr(response, "usage", None),
        "response": response,
    }


def embed_platform_outputs(
    outputs: Sequence[Any],
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    client: Any = None,
) -> List[Dict[str, Any]]:
    return [embed_platform_output(output, model=model, api_key=api_key, client=client) for output in outputs]
