import os
import json
from typing import Any, Dict
from model_client import GeminiClient
from model_models import JsonResponse

def extract_json(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"))
    model = client.get_model("gemini-1.5-flash")  # Optimized for structured output

    text_to_process = payload.get("text", "")
    if not text_to_process:
        raise ValueError("Payload must contain 'text' for JSON extraction.")

    prompt = (
        "Extract structured JSON from the following text. "
        "The JSON should represent the key entities and their properties. "
        "Ensure the output is valid JSON, and only output the JSON. "
        "\n\nText: " + text_to_process
    )

    response = model.generate_content(prompt)
    try:
        # Assuming the model directly returns JSON as text
        json_output = json.loads(response.text.strip())
        return {"json_data": json_output}
    except json.JSONDecodeError:
        # If the model doesn't return perfect JSON, try to find a JSON block
        # This is a basic attempt; more robust parsing might be needed for real-world scenarios
        start_idx = response.text.find('{')
        end_idx = response.text.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                json_output = json.loads(response.text[start_idx : end_idx + 1])
                return {"json_data": json_output}
            except json.JSONDecodeError:
                pass # Fallback to empty if still unable to decode
    return {"json_data": {}} # Return empty dict if extraction fails
