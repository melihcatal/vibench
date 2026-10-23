from typing import Any, Dict, List


def create_model_request(model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "model_id": model_id,
        "input_data": input_data,
    }


def parse_model_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if 'output' in response:
        return response['output']
    return {}


def normalize_model_output(output: Dict[str, Any]) -> Dict[str, Any]:
    normalized_output = {}
    for key, value in output.items():
        normalized_output[key.lower()] = value
    return normalized_output