from typing import Dict, Any

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if not k.startswith('__')}