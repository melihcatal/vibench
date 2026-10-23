import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _load_event_payload(event):
    if event is None:
        return {}
    if isinstance(event, str):
        return json.loads(event)
    if isinstance(event, dict):
        body = event.get('body')
        if isinstance(body, str):
            try:
                parsed = json.loads(body)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass
        return event
    return {}


def normalize_document_payload(document, document_id_name='document_id'):
    if not isinstance(document, dict):
        raise ValueError('document must be a dict')
    return {k: v for k, v in document.items() if v is not None and k != document_id_name}


@dataclass
class UpsertDocumentRequest:
    document_id: str
    document: Dict[str, Any]

    @classmethod
    def from_event(cls, event):
        payload = _load_event_payload(event)
        return cls(document_id=str(payload['document_id']), document=payload.get('document', payload))


@dataclass
class FetchDocumentRequest:
    document_id: str

    @classmethod
    def from_event(cls, event):
        payload = _load_event_payload(event)
        return cls(document_id=str(payload['document_id']))


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any

    @classmethod
    def from_event(cls, event):
        payload = _load_event_payload(event)
        return cls(field_name=str(payload['field_name']), field_value=payload['field_value'])


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None

    @classmethod
    def from_event(cls, event):
        payload = _load_event_payload(event)
        return cls(document_id=str(payload['document_id']), updates=dict(payload.get('updates', {})), expected_version=payload.get('expected_version'))


def normalize_update_expression(updates, version_attr):
    if not isinstance(updates, dict) or not updates:
        raise ValueError('updates must be a non-empty dict')
    names = {}
    values = {}
    parts = []
    for idx, (key, value) in enumerate(updates.items()):
        name_key = f'#k{idx}'
        value_key = f':v{idx}'
        names[name_key] = key
        values[value_key] = value
        parts.append(f'{name_key} = {value_key}')
    if version_attr not in updates:
        name_key = '#version'
        value_key = ':version_inc'
        names[name_key] = version_attr
        values[value_key] = 1
        parts.append(f'{name_key} = if_not_exists({name_key}, :zero) + {value_key}')
        values[':zero'] = 0
    return 'SET ' + ', '.join(parts), names, values


def upsert_result(document_id, item):
    return {'document_id': document_id, 'item': item, 'status': 'upserted'}


def fetch_result(document_id, item, found=True):
    return {'document_id': document_id, 'item': item, 'found': found}


def query_result(items):
    return {'items': items, 'count': len(items)}


def conditional_update_result(item):
    return {'item': item, 'updated': True}
