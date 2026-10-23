import json
from typing import Any, Dict


def normalize_chat_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize OpenAI chat response to a simple dict format.

    Expected structure: {'choices': [{'message': {'content': '...'}}]}
    """
    try:
        return {
            "role": "assistant",
            "content": response["choices"][0]["message"]["content"]
        }
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Malformed OpenAI response") from exc


def normalize_chat_completion(
    request: Dict[str, Any], response: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a normalized envelope for a chat completion call.

    Returns: {'request': {...}, 'response': {...}}
    """
    return {
        "request": request,
        "response": normalize_chat_response(response)
    }

if __name__ == "__main__":
    # Example usage (requires OPENAI_API_KEY set in env)
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": "Hello"}])
    print(json.dumps(normalize_chat_completion({"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Hello"}]}, resp), indent=2))
