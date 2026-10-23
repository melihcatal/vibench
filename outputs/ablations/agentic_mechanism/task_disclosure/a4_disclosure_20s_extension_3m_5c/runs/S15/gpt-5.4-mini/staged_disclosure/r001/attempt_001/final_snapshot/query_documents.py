import json
import os
import sys
from typing import Any, Dict, List, Optional

from pinecone import Pinecone


def _get_env(name: str, required: bool = True, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value or ""


def _coerce_value(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _build_filter(field: str, raw_value: str) -> Dict[str, Any]:
    return {field: {"$eq": _coerce_value(raw_value)}}


def query_documents(field: str, value: str, namespace: Optional[str] = None, top_k: int = 10) -> List[Dict[str, Any]]:
    api_key = _get_env("PINECONE_API_KEY")
    index_name = _get_env("PINECONE_INDEX_NAME")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    query_kwargs: Dict[str, Any] = {
        "vector": [0.0],
        "top_k": top_k,
        "filter": _build_filter(field, value),
        "include_metadata": True,
    }
    if namespace:
        query_kwargs["namespace"] = namespace
    response = index.query(**query_kwargs)
    matches = getattr(response, "matches", None) or response.get("matches", [])
    return [
        {
            "id": match.get("id") if isinstance(match, dict) else getattr(match, "id", None),
            "score": match.get("score") if isinstance(match, dict) else getattr(match, "score", None),
            "metadata": match.get("metadata") if isinstance(match, dict) else getattr(match, "metadata", None),
        }
        for match in matches
    ]


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: query_documents.py <field> <value> [namespace] [top_k]")
    field = sys.argv[1]
    value = sys.argv[2]
    namespace = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    top_k = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    results = query_documents(field, value, namespace=namespace, top_k=top_k)
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
