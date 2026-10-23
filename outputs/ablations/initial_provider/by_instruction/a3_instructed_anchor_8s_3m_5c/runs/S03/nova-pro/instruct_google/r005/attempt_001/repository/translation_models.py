from typing import List, Dict

def normalize_translation_response(response: Dict) -> str:
    return response['translatedText']

def batch_normalize_translation_responses(responses: List[Dict]) -> List[str]:
    return [normalize_translation_response(response) for response in responses]