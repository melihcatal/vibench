import base64
import os
from typing import Any, Dict, Union


def get_document_payload(source: Union[bytes, str]) -> bytes:
    if isinstance(source, bytes):
        return source
    if os.path.exists(source):
        with open(source, 'rb') as f:
            return f.read()
    return base64.b64decode(source)


def normalize_text(value: Any) -> str:
    if value is None:
        return ''
    return ' '.join(str(value).split())


def confidence_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, score / 100.0 if score > 1 else score))
