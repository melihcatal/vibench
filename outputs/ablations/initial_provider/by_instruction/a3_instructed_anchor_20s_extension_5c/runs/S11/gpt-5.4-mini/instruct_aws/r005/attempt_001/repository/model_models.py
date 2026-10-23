import json


def normalize_prompt(prompt: str) -> str:
    return prompt.strip()


def build_messages(prompt: str):
    return [{"role": "user", "content": [{"type": "text", "text": normalize_prompt(prompt)}]}]


def extract_text(response) -> str:
    if isinstance(response, dict):
        if "output" in response and isinstance(response["output"], dict):
            blocks = response["output"].get("message", {}).get("content", [])
            return "".join(block.get("text", "") for block in blocks if isinstance(block, dict))
        if "content" in response:
            return "".join(block.get("text", "") for block in response.get("content", []) if isinstance(block, dict))
    return str(response)


def json_body(data) -> bytes:
    return json.dumps(data).encode("utf-8")
