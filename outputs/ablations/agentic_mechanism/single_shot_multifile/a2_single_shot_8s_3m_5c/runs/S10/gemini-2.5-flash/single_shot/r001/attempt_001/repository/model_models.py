from typing import Dict, Any

def normalize_response(response: Any, provider: str) -> Dict[str, Any]:
    normalized = {"text": "", "model_id": "", "finish_reason": None}

    if provider == "openai":
        if response.choices:
            normalized["text"] = response.choices[0].message.content
            normalized["model_id"] = response.model
            normalized["finish_reason"] = response.choices[0].finish_reason
    elif provider == "anthropic":
        if response.content:
            normalized["text"] = response.content[0].text
            normalized["model_id"] = response.model
            normalized["finish_reason"] = response.stop_reason
    elif provider == "google":
        if response.candidates:
            normalized["text"] = response.candidates[0].content.parts[0].text
            normalized["model_id"] = response.model
            normalized["finish_reason"] = str(response.candidates[0].finish_reason)
    return normalized