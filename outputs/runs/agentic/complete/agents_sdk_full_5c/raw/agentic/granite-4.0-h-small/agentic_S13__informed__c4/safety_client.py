import os
from typing import Optional
import requests
from safety_models import (ModerationRequest, ModerationResponse,
                             CategoryScore, UnsafeSpan)

# Perspective API integration (concrete third-party provider)
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
BASE_URL = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'

def _perspective_post(text: str) -> dict:
    """Send a single text to Perspective API and return raw JSON."""
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"SEVERITY": {}}
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY
    }
    resp = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def moderate_single(text: str) -> ModerationResponse:
    """Return normalized moderation response for a single piece of text."""
    raw = _perspective_post(text)
    # Perspective returns attributeScores -> SEVERITY -> summaryScore -> value
    attr = raw.get('attributeScores', {}).get('SEVERITY', {})
    summary = attr.get('summaryScore', {})
    value = summary.get('value')
    request = ModerationRequest(text=text)
    # Map Perspective SEVERITY score to unified CategoryScore list
    categories = [
        CategoryScore(category='harassment', score=value),
        # Add other categories as needed; currently Perspective only provides SEVERITY
    ]
    return ModerationResponse(request=request, categories=categories, raw=raw)

def moderate_batch(texts: list[str]) -> list[ModerationResponse]:
    """Batch version of moderate_single using the same provider."""
    requests = [ModerationRequest(text=t) for t in texts]
    payload = {
        "comment": {"text": ""},
        "requestedAttributes": {"SEVERITY": {}}
    }
    # Perspective API expects a list of comments for batch; we'll call single calls for simplicity
    responses = [_perspective_post(t) for t in texts]
    batch = []
    for req, raw in zip(requests, responses):
        attr = raw.get('attributeScores', {}).get('SEVERITY', {})
        summary = attr.get('summaryScore', {})
        value = summary.get('value')
        categories = [
            CategoryScore(category='harassment', score=value),
        ]
        batch.append(ModerationResponse(request=req, categories=categories, raw=raw))
    return batch

def get_unsafe_spans(text: str) -> list[UnsafeSpan]:
    """Stub placeholder for unsafe span extraction using Perspective API.
    Perspective does not return span data, so this returns an empty list."""
    return []
