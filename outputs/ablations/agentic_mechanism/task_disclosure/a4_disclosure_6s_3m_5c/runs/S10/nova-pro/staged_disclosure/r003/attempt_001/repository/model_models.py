from typing import Any, Dict, List


def create_inference_request(model_id: str, prompt: str, max_tokens: int) -> Dict[str, Any]:
    return {
        'model': model_id,
        'prompt': prompt,
        'max_tokens': max_tokens
    }


def parse_inference_response(response: Dict[str, Any]) -> str:
    return response.get('generated_text', '')


def normalize_model_family(model_family: str) -> str:
    return model_family.lower().replace(' ', '-')


def select_model_family(model_families: List[str], preference: str) -> str:
    normalized_preference = normalize_model_family(preference)
    for family in model_families:
        if normalize_model_family(family) == normalized_preference:
            return family
    return model_families[0] if model_families else ''