from __future__ import annotations

import re
from typing import Any, Dict

from google.cloud import aiplatform

from observability_models import MetricAnnotationRequest


def metric_annotation_safety(text: str, locale: str = "en") -> Dict[str, Any]:
    req = MetricAnnotationRequest(text=text, locale=locale)
    client = aiplatform.gapic.PredictionServiceClient()
    unsafe_patterns = [r"<script", r"javascript:", r"drop\s+table", r"select\s+.*from"]
    unsafe = any(re.search(p, req.text, flags=re.IGNORECASE) for p in unsafe_patterns)
    return {
        "locale": req.locale,
        "unsafe": unsafe,
        "provider": "google-cloud-aiplatform",
        "model": "gemini-1.5-pro",
        "prediction_client": client.__class__.__name__,
    }
