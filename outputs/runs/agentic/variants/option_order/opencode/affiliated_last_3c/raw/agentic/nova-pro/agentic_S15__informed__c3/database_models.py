from typing import Dict, Any


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in item.items() if v is not None}
