from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _image_bytes(payload: Dict[str, Any]) -> bytes:
    value = payload.get('image_bytes')
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    raise ValueError('image_bytes is required')


def normalized_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config = dict(config or {})
    if 'endpoint' not in config:
        config['endpoint'] = config.get('azure_vision_endpoint')
    if 'api_key' not in config:
        config['api_key'] = config.get('azure_vision_api_key')
    return config


def tags_to_labels(tags: Any, limit: int = 10) -> List[Dict[str, Any]]:
    items = getattr(tags, 'list', tags)
    items = sorted(items, key=lambda tag: tag.confidence, reverse=True)
    return [{'name': tag.name, 'confidence': tag.confidence} for tag in items[:limit]]


def captions_to_text(captions: Any) -> str:
    items = getattr(captions, 'list', captions)
    if not items:
        return ''
    best = sorted(items, key=lambda caption: caption.confidence, reverse=True)[0]
    return best.text


def read_text_lines(read_result: Any) -> List[str]:
    blocks = getattr(read_result, 'blocks', [])
    lines: List[str] = []
    for block in blocks:
        for line in getattr(block, 'lines', []):
            lines.append(line.text)
    return lines


def safety_categories_to_risks(categories: Any) -> List[Dict[str, Any]]:
    items = getattr(categories, 'list', categories)
    return [{'name': category.name, 'severity': category.severity} for category in items]
