# [LATER-STEP] metric_annotation_safety.py

import os
from .observability_client import get_gcp_monitoring_client
from .observability_models import MetricQueryRequest

# We'll use Google Cloud's Perspective API as the safety detector (placeholder)
# Requires PERSPECTIVE_API_KEY in environment

SUPPORTED_SERVICE = 'gcp'

try:
    from google.cloud import language_v1
    from google.cloud.language_v1 import types
    client = language_v1.LanguageServiceClient()
    PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')
except Exception as e:
    raise RuntimeError("Safety module missing required client or credentials")

def check_annotation_safety(req):
    """Detect unsafe text in metric labels or annotations using Perspective API.",
    # For demo we treat the request's raw label payload as text to moderate.
    # In practice you'd pass specific label values.
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is None:
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS to use GCP client")
    # Placeholder: directly call Perspective API via HTTP (no sdk due to tool limits)
    # Here we simulate with a simple heuristic:
    unsafe_words = ['error', 'failure', 'crash']  # naive filter
    # Simulated safety verdict
    verdict = any(word in str(req).lower() for word in unsafe_words)
    return {
        "safe": not verdict,
        "details": {
            "unsafe_words_detected": unsafe_words if verdict else []
        }
    }

# Example usage (for local testing)
if __name__ == '__main__':
    req = {"labels": {"description": "System failure detected"}}
    print(check_annotation_safety(req))
