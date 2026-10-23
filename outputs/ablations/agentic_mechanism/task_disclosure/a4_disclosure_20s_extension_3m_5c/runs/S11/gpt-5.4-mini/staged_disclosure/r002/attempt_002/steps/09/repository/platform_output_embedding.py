import base64
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union
from urllib import error, request


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_URL = "https://api.openai.com/v1/embeddings"


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    embedding: List[float]
    model: str
    provider: str = "openai"


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (list, tuple, set)):
        return json.dumps(list(value), ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _extract_output_text(platform_output: Any) -> str:
    if isinstance(platform_output, str):
        return platform_output
    if isinstance(platform_output, bytes):
        return platform_output.decode("utf-8", errors="replace")
    if isinstance(platform_output, dict):
        for key in ("output", "text", "content", "message", "result"):
            if key in platform_output:
                extracted = _extract_output_text(platform_output[key])
                if extracted:
                    return extracted
        return _normalize_text(platform_output)
    if isinstance(platform_output, (list, tuple)):
        parts = [_extract_output_text(item) for item in platform_output]
        return "\n".join(part for part in parts if part)
    return _normalize_text(platform_output)


def _openai_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _call_openai_embeddings(texts: Sequence[str], model: str, api_key: str) -> List[List[float]]:
    payload = json.dumps({"model": model, "input": list(texts)}).encode("utf-8")
    req = request.Request(OPENAI_API_URL, data=payload, headers=_openai_headers(api_key), method="POST")
    try:
        with request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        raise RuntimeError(f"OpenAI embeddings request failed: {exc.code} {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenAI embeddings request error: {exc.reason}") from exc

    if "data" not in data:
        raise RuntimeError("OpenAI embeddings response missing data")

    items = sorted(data["data"], key=lambda item: item.get("index", 0))
    embeddings: List[List[float]] = []
    for item in items:
        embedding = item.get("embedding")
        if not isinstance(embedding, list):
            raise RuntimeError("OpenAI embeddings response has invalid embedding")
        embeddings.append([float(x) for x in embedding])
    return embeddings


def embed_platform_output(platform_output: Any, api_key: Optional[str] = None, model: Optional[str] = None) -> EmbeddingResult:
    text = _extract_output_text(platform_output).strip()
    if not text:
        text = ""
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    model_name = model or OPENAI_EMBEDDING_MODEL
    embedding = _call_openai_embeddings([text], model_name, api_key)[0]
    return EmbeddingResult(text=text, embedding=embedding, model=model_name)


def embed_platform_outputs(platform_outputs: Iterable[Any], api_key: Optional[str] = None, model: Optional[str] = None) -> List[EmbeddingResult]:
    texts = [_extract_output_text(item).strip() for item in platform_outputs]
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    model_name = model or OPENAI_EMBEDDING_MODEL
    vectors = _call_openai_embeddings(texts, model_name, api_key)
    return [EmbeddingResult(text=texts[i], embedding=vectors[i], model=model_name) for i in range(len(texts))]


def stable_embedding_fingerprint(embedding: Sequence[float]) -> str:
    raw = ",".join(f"{x:.10f}" for x in embedding).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def serialize_embedding_result(result: EmbeddingResult) -> str:
    return json.dumps({"provider": result.provider, "model": result.model, "text": result.text, "embedding": result.embedding, "fingerprint": stable_embedding_fingerprint(result.embedding)}, ensure_ascii=False)
