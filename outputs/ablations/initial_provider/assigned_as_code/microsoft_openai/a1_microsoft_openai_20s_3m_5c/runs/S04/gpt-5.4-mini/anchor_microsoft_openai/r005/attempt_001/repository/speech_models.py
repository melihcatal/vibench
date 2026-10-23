from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _items(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_transcript_payload(payload):
    if isinstance(payload, dict):
        return payload
    return {'text': str(payload)}


def extract_transcript_text(payload):
    payload = normalize_transcript_payload(payload)
    if payload.get('combinedRecognizedPhrases'):
        return ' '.join(part.get('nBest', [{}])[0].get('display', '') for part in payload['combinedRecognizedPhrases']).strip()
    if payload.get('recognizedPhrases'):
        return ' '.join(part.get('nBest', [{}])[0].get('display', '') for part in payload['recognizedPhrases']).strip()
    return payload.get('text', '')


def extract_timestamps(payload):
    payload = normalize_transcript_payload(payload)
    out = []
    for segment in _items(payload.get('recognizedPhrases') or payload.get('combinedRecognizedPhrases')):
        best = segment.get('nBest', [{}])[0]
        out.append({'speaker': segment.get('speaker'), 'text': best.get('display', ''), 'offset': segment.get('offset'), 'duration': segment.get('duration')})
    return out


@dataclass
class TranslationRequest:
    text: str
    to: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class SummaryRequest:
    transcript: str


@dataclass
class EmbeddingRequest:
    segments: List[str]
