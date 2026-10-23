from dataclasses import dataclass


def normalize_text_payload(payload):
    if isinstance(payload, dict):
        if 'text' in payload:
            return {'text': str(payload['text'])}
        if 'ssml' in payload:
            return {'ssml': str(payload['ssml'])}
    return {'text': str(payload)}


def normalize_voice_selection(payload):
    payload = payload or {}
    return {
        'locale': payload.get('locale'),
        'voice': payload.get('voice'),
    }


@dataclass
class SpeechRequest:
    text: str = ''
    ssml: str = ''
    voice: str = ''
    locale: str = ''
    prosody_rate: str = ''
    prosody_pitch: str = ''


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str = 'audio/mpeg'
