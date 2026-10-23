from dataclasses import dataclass


def normalize_text(payload):
    if isinstance(payload, dict):
        return payload.get('text') or payload.get('script') or payload.get('ssml') or ''
    return payload if payload is not None else ''


def normalize_locale(payload, default='en-US'):
    if isinstance(payload, dict):
        return payload.get('locale') or payload.get('language') or default
    return default


def normalize_voice(payload, default=None):
    if isinstance(payload, dict):
        return payload.get('voice') or payload.get('voice_name') or default
    return default


def normalize_output_format(payload, default='audio/mpeg'):
    if isinstance(payload, dict):
        return payload.get('content_type') or payload.get('format') or default
    return default


@dataclass
class SpeechRequest:
    text: str
    locale: str = 'en-US'
    voice: str = 'en-US-JennyNeural'
    content_type: str = 'audio/mpeg'


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str
