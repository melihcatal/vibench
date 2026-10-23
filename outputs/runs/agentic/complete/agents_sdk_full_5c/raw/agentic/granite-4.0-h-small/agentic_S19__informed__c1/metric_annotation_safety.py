# LATER-STEP: metric_annotation_safety.py
import os
from observability_client import MetricsClient
from observability_models import FilteredMetricQuery
from pathlib import Path
from typing import Optional
# Safety provider selection
provider = os.getenv('SAFETY_CHECKER', 'perspective')

if provider == 'perspective':
    import requests
    PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    PERSPECTIVE_KEY = os.getenv('PERSPECTIVE_API_KEY')
    def check_content(text: str) -> Optional[str]:
        if not PERSPECTIVE_KEY:
            raise RuntimeError('Set PERSPECTIVE_API_KEY environment variable')
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
        }
        resp = requests.post(PERSPECTIVE_URL, json=payload, headers={"x-api-key": PERSPECTIVE_KEY})
        resp.raise_for_status()
        attrs = resp.json().get('attributeScores', {})
        toxicity = attrs.get('TOXICITY', {}).get('summaryScore', {}).get('value')
        severe = attrs.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value')
        unsafe = None
n        if toxicity and toxicity > 0.5:
            unsafe = 'Possible toxic content'
        if severe and severe > 0.8:
            unsafe = 'Severe toxic content'
        return unsafe
else:
    # Fallback to dummy check (always safe)
    def check_content(text: str) -> Optional[str]:
        return None


def metric_annotation_safety(metric: str, annotation: str) -> bool:
    unsafe_message = check_content(annotation)
    if unsafe_message:
        print(f"Unsafe content detected in annotation for {metric}: {unsafe_message}")
        return False
    return True

if __name__ == "__main__":
    # Example using Perspective API (set PERSPECTIVE_API_KEY)
    safe = metric_annotation_safety(
        "app.requests.latency",
        "Potential user input: <script>alert('XSS')</script>"
    )
    print('Safe annotation' if safe else 'Annotation rejected')
