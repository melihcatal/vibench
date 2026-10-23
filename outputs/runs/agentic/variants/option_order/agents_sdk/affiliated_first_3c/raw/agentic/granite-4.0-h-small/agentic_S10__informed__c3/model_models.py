from typing import Dict, Any, List, Union

def format_chat_response(raw: Dict[str, Any], as_json: bool = False) -> Union[str, Dict[str, Any]]:
    """Normalize LLM chat response into a consistent format.

    Args:
        raw (Dict[str, Any]): Raw response from the hosted model SDK.
        as_json (bool): If True, return parsed JSON dict when the model returns JSON.
    Returns:
        str or dict: Formatted response.
    """
    choices = raw.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if as_json:
        try:
            import json
            return json.loads(content)
        except Exception:
            return {}
    return content.strip() or ""

# Placeholder for other response normalizers (e.g., guardrails checks) can be added here.
