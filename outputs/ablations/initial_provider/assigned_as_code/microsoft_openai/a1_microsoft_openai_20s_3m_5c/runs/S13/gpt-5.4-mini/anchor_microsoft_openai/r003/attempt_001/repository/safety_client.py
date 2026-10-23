import os


def get_safety_config(config=None):
    base = dict(config or {})
    base.setdefault('endpoint', os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'))
    base.setdefault('api_key', os.environ.get('AZURE_CONTENT_SAFETY_API_KEY'))
    return base


def get_text(payload):
    if isinstance(payload, dict):
        for key in ('text', 'message', 'content'):
            value = payload.get(key)
            if value is not None:
                return str(value)
    return str(payload)


def get_texts(payload):
    if isinstance(payload, dict):
        for key in ('texts', 'messages', 'items'):
            value = payload.get(key)
            if isinstance(value, list):
                return [get_text(item) for item in value]
    if isinstance(payload, list):
        return [get_text(item) for item in payload]
    return [get_text(payload)]


def severity_score(category):
    return getattr(category, 'severity', 0) / 7
