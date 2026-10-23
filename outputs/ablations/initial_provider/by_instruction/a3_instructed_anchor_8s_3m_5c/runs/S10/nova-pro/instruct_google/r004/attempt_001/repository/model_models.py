from typing import Dict, Any

def normalize_request(instance: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    return {"instances": [instance], "parameters": parameters}

def parse_response(response: Dict[str, Any]) -> str:
    return response['predictions'][0]['content']