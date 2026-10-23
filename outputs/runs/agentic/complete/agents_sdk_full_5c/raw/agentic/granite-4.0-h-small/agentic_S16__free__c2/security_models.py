from typing import Dict, Any, Optional

class SecretPayload(NamedTuple):
    name: str
    version: Optional[str] = None
    payload: Any = None

class SecretRequest(NamedTuple):
    name: str
    version: Optional[str] = None
    labels: Optional[Dict[str, str]] = None

class SecretResponse(NamedTuple):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

def normalize_secret_labels(labels: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Convert labels to lowercase keys and strip whitespace."""
    if not labels:
        return {}
    normalized = {}
    for k, v in labels.items():
        nk = k.strip().lower()
        nv = v.strip() if v else ''
        normalized[nk] = nv
    return normalized
