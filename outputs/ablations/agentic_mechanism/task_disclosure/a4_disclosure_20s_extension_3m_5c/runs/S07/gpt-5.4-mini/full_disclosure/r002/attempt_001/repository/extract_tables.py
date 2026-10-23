import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib import request as urllib_request
from urllib.error import HTTPError, URLError


OPENAI_TABLE_MODEL = os.environ.get("OPENAI_TABLE_MODEL", "gpt-4o-mini")
OPENAI_API_URL = "https://api.openai.com/v1/responses"


def _load_document_bytes(document: Union[str, bytes, Path]) -> bytes:
    if isinstance(document, bytes):
        return document
    return Path(document).read_bytes()


def _to_data_url(document_bytes: bytes, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64.b64encode(document_bytes).decode('ascii')}"


def extract_tables(
    document: Union[str, bytes, Path],
    api_key: Optional[str] = None,
    mime_type: str = "application/pdf",
) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    document_bytes = _load_document_bytes(document)
    payload: Dict[str, Any] = {
        "model": OPENAI_TABLE_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all tables from this document as structured JSON with table names, rows, columns, and cell text. Preserve row structure and cell ordering.",
                    },
                    {
                        "type": "input_image",
                        "image_url": _to_data_url(document_bytes, mime_type)
                        if mime_type.startswith("image/")
                        else {"type": "input_text", "text": "Document bytes provided separately."},
                    },
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }

    req = urllib_request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"OpenAI API error: {exc.read().decode('utf-8', 'ignore')}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


__all__ = ["extract_tables", "OPENAI_TABLE_MODEL", "OPENAI_API_URL"]
