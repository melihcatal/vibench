import json
from typing import Any, Dict, List


def build_system_user_messages(
    system_prompt: str, user_prompt: str
) -> List[Dict[str, str]]:
    """Build standard system and user messages for chat completion."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def parse_json_response(content: str) -> Any:
    """Safely parse JSON from LLM output."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None
