from typing import Any, Dict

# Helper to normalize request payloads
# Provider identified in code
PROVIDER = "Mistral"


def build_chat_payload(
    messages: list[dict[str, Any]], model: str = "mistral-large"
) -> dict[str, Any]:
    return {"model": model, "messages": messages}


# Helper to extract structured result from response


def extract_result(response: dict[str, Any]) -> Any:
    # Assuming the model returns a JSON string in the first message content
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "{}")
    import json

    return json.loads(content)
