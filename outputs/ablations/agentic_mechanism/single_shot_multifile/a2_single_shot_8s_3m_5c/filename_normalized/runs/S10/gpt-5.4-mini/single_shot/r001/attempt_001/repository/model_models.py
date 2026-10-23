import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class ChatRequest:
    model: str
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    max_tokens: Optional[int] = None

    def to_kwargs(self) -> Dict[str, Any]:
        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': self.user_prompt},
        ]
        payload: Dict[str, Any] = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature,
        }
        if self.max_tokens is not None:
            payload['max_tokens'] = self.max_tokens
        return payload


def extract_message_text(response: Any) -> str:
    choices = getattr(response, 'choices', None) or []
    if not choices:
        return ''
    message = getattr(choices[0], 'message', None)
    if message is None:
        return ''
    content = getattr(message, 'content', None)
    if isinstance(content, list):
        return ''.join(part.get('text', '') if isinstance(part, dict) else str(part) for part in content)
    return content or ''


def extract_stream_delta(chunk: Any) -> str:
    choices = getattr(chunk, 'choices', None) or []
    if not choices:
        return ''
    delta = getattr(choices[0], 'delta', None)
    if delta is None:
        return ''
    content = getattr(delta, 'content', None)
    if isinstance(content, list):
        return ''.join(part.get('text', '') if isinstance(part, dict) else str(part) for part in content)
    return content or ''


def normalize_text_output(text: str) -> str:
    return ' '.join((text or '').strip().split())


def parse_json_text(text: str) -> Dict[str, Any]:
    cleaned = (text or '').strip()
    if cleaned.startswith('```'):
        cleaned = cleaned.strip('`')
        cleaned = cleaned.replace('json\n', '', 1) if cleaned.startswith('json\n') else cleaned
    return json.loads(cleaned)
