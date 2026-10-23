from typing import Any, Dict

# Define local request, response, and normalization helpers
def normalize_response(response: Dict[str, Any]) -> str:
    return response['output_text']