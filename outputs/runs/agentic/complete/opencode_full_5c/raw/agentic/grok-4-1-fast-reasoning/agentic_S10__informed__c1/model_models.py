from typing import List, Dict, Any, Iterator

MODEL_FAMILY = "mistral-large-latest"

DEFAULT_PARAMS = {"temperature": 0.3, "max_tokens": 1000}


def create_system_message(content: str) -> Dict[str, str]:
    return {"role": "system", "content": content}


def create_user_message(content: str) -> Dict[str, str]:
    return {"role": "user", "content": content}


def normalize_response(response: Any) -> str:
    return response.choices[0].message.content.strip()
