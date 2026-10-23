"""
Local configuration and client helper utilities for Text Content Safety.
Uses Google Cloud's Perspective API for content moderation.
"""
import os
from typing import List, Dict, Optional
from googleapiclient import discovery
from google.api_core import retry
from googleapiclient.errors import HttpError
from safety_models import (
    PerspectiveRequest,
    TextModerationResult,
    TextRedactionResult,
    build_perspective_request,
    normalize_perspective_response
)


class SafetyClient:
    """Client for interacting with Google Cloud's Perspective API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
        self.client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=self.api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False
        )

    @retry.Retry()
    def analyze_text(self, text: str, categories: List[str]) -> TextModerationResult:
        """Analyze text for content safety using Perspective API."""
        request_body: PerspectiveRequest = build_perspective_request(text, categories)
        try:
            response = self.client.comments().analyze(body=request_body).execute()
            return normalize_perspective_response(response, text)
        except HttpError as e:
            raise Exception(f"Perspective API request failed: {e}")

    def redact_unsafe_spans(self, text: str, categories: List[str], threshold: float = 0.7) -> TextRedactionResult:
        """Redact unsafe spans from text based on Perspective API scores."""
        result = self.analyze_text(text, categories)
        unsafe_spans = []
        redacted_text = text
        
        # Simulate span redaction (Perspective API does not provide spans directly)
        for score in result.scores:
            if score.score >= threshold:
                unsafe_spans.append({
                    "start": 0,
                    "end": len(text),
                    "category": score.category,
                    "score": score.score
                })
                redacted_text = "[REDACTED]"
        
        return TextRedactionResult(
            original_text=text,
            redacted_text=redacted_text,
            unsafe_spans=unsafe_spans
        )