from dataclasses import dataclass


@dataclass
class PlatformPrompt:
    text: str
    locale: str = "en"


@dataclass
class PlatformResponse:
    text: str
    model_id: str
    usage: dict
    metadata: dict


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def build_bedrock_messages(prompt: str):
    return [
        {"role": "user", "content": [{"type": "text", "text": normalize_text(prompt)}]}
    ]
