from typing import Dict, Any, Optional
import time

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = document.copy()
    normalized["updated_at"] = int(time.time())
    normalized["version"] = normalized.get("version", 0) + 1
    return normalized

def denormalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if not k.startswith("_")}