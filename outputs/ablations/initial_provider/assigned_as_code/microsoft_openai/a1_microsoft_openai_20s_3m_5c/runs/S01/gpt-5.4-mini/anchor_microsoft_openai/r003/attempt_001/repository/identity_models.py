import re


def normalize_email(value):
    return value.strip().lower()


def normalize_locale(value):
    return (value or 'en').replace('_', '-').lower()


def normalize_text(value):
    return ' '.join((value or '').strip().split())


def build_email_password_payload(payload):
    payload = dict(payload or {})
    if 'email' in payload:
        payload['email'] = normalize_email(payload['email'])
    if 'locale' in payload:
        payload['locale'] = normalize_locale(payload['locale'])
    if 'password' in payload and isinstance(payload['password'], str):
        payload['password'] = payload['password']
    return payload


def build_note_document(payload):
    payload = dict(payload or {})
    payload['email'] = normalize_email(payload['email']) if 'email' in payload else None
    payload['note'] = normalize_text(payload.get('note'))
    payload['locale'] = normalize_locale(payload.get('locale'))
    return payload
