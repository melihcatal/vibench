from dataclasses import dataclass
from html import escape
from typing import Optional


@dataclass(frozen=True)
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    style: Optional[str] = None
    rate: Optional[str] = None
    pitch: Optional[str] = None


def normalize_text(text: str) -> str:
    return ' '.join((text or '').split())


def normalize_ssml(text: str) -> str:
    return normalize_text(text)


def ssml_from_request(request: SpeechRequest) -> str:
    locale = request.locale or 'en-US'
    voice = request.voice or 'en-US-JennyNeural'
    body = escape(request.text)
    prosody = []
    if request.rate:
        prosody.append(f'rate="{escape(request.rate)}"')
    if request.pitch:
        prosody.append(f'pitch="{escape(request.pitch)}"')
    prosody_attrs = ' '.join(prosody)
    prosody_open = f'<prosody {prosody_attrs}>' if prosody_attrs else '<prosody>'
    return (
        f'<speak version="1.0" xml:lang="{escape(locale)}" xmlns="http://www.w3.org/2001/10/synthesis">'
        f'<voice name="{escape(voice)}">{prosody_open}{body}</prosody></voice>'
        f'</speak>'
    )
