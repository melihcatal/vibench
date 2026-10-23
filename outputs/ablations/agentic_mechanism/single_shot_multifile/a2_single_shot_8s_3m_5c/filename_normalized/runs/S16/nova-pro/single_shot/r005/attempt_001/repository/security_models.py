from typing import Dict, Any

def normalize_secret_response(response) -> Dict[str, Any]:
    return {'data': response.payload.data.decode('UTF-8') if response.payload else None}

def parse_json_secret_response(response) -> Dict[str, Any]:
    return json.loads(response.payload.data) if response.payload else {}