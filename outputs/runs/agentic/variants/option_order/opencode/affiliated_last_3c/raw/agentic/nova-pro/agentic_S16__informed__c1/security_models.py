from typing import Any, Dict


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "SecretString": response.get("SecretString", ""),
        "ARN": response.get("ARN", ""),
        "Name": response.get("Name", ""),
        "VersionId": response.get("VersionId", ""),
    }
