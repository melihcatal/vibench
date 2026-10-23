from typing import Dict


def normalize_response(response: Dict) -> Dict:
    return {
        "object_name": response.get("name"),
        "metadata": response.get("metadata", {}),
    }