import json


def clean_text(value):
    return "" if value is None else str(value).strip()


def anthropic_messages_prompt(system, user, max_tokens=512, temperature=0.2):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": int(max_tokens),
        "temperature": float(temperature),
        "system": clean_text(system),
        "messages": [{"role": "user", "content": [{"type": "text", "text": clean_text(user)}]}],
    })


def parse_anthropic_text(body):
    data = json.loads(body)
    content = data.get("content", [])
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "".join(parts).strip()


def json_prompt(system, user, max_tokens=512, temperature=0.0):
    return anthropic_messages_prompt(system, user, max_tokens=max_tokens, temperature=temperature)


def safe_json_loads(value):
    text = clean_text(value)
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise
