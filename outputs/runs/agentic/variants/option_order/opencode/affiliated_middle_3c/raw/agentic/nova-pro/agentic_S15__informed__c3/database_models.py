from typing import Dict


def normalize_item(item: Dict) -> Dict:
    return {k: v["S"] for k, v in item.items()}


def normalize_response(response: Dict) -> Dict:
    return {k: normalize_item(v["Item"]) for k, v in response.items() if k == "Item"}
