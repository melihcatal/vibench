from typing import Dict, Any

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {"secret_value": response.get("SecretString") or response.get("SecretBinary").decode("utf-8")}