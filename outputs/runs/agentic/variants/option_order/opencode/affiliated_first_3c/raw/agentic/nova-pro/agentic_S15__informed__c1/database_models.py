from typing import Dict


def normalize_item(item: Dict) -> Dict:
    return {k: v for k, v in item.items() if v is not None}


def normalize_response(response: Dict) -> Dict:
    return {k: v for k, v in response.items() if v is not None}
