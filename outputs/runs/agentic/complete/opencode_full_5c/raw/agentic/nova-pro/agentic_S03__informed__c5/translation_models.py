from typing import List, Dict


def normalize_response(response: List[Dict]) -> List[str]:
    return [item["translations"][0]["text"] for item in response]
