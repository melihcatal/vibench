from typing import Any, Dict


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {"output": response["output"], "metadata": response["metadata"]}
