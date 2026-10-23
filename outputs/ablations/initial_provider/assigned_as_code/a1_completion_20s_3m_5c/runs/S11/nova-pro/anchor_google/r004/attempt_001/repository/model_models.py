from typing import Any, Dict

def model_models(response: Dict[str, Any]):
    return response['predictions'][0]['output']

def normalize_response(response: Dict[str, Any]):
    return {
        'output': model_models(response),
        'metadata': response.get('metadata', {}),
    }