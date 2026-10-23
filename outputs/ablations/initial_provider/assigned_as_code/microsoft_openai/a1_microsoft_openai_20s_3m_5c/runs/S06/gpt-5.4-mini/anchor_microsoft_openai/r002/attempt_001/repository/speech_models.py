from dataclasses import dataclass


def normalize_text_payload(payload):
    if isinstance(payload, dict):
        return dict(payload)
    return {'text': str(payload)}


def normalize_voice_payload(payload):
    data = normalize_text_payload(payload)
    if 'locale' not in data and 'language' in data:
        data['locale'] = data['language']
    return data


@dataclass
class SpeechResult:
    audio_bytes: bytes
    content_type: str = 'audio/mpeg'


@dataclass
class VoiceSelection:
    name: str
    locale: str
