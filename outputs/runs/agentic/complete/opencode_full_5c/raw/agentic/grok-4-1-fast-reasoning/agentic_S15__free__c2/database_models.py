import decimal
from typing import Any, Dict, List


def to_dynamo_item(document: Dict[str, Any]) -> Dict[str, Any]:
    item = document.copy()
    if "id" in item:
        item["id"] = str(item["id"])
    if "version" not in item:
        item["version"] = 1
    else:
        item["version"] = int(item["version"])
    return item


def from_dynamo_item(item: Dict[str, Any]) -> Dict[str, Any]:
    if item is None:
        return None

    def decode(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: decode(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [decode(v) for v in value]
        elif isinstance(value, decimal.Decimal):
            return int(value) if value == int(value) else float(value)
        else:
            return value

    return decode(item)
