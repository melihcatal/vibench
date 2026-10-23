from typing import Dict, List


def normalize_response(response: Dict) -> str:
    return response["TranslatedText"]


def batch_normalize_responses(responses: List[Dict]) -> List[str]:
    return [normalize_response(response) for response in responses]
