import json
from typing import List, Dict, Any
from .observability_models import SafeCheckResult
from .observability_client import build_client # placeholder import for uniform structure

SERVICE = "perspective-api"

def check_safe(log_events: List[Dict[str, Any]]) -> SafeCheckResult:
    """Run selected log message text through a text safety / moderation service.",
    # For demo we use Perspective API (textmoderation).
    # Build concatenated text from recent events (or single event)
    texts = [ev["msg"] for ev in log_events]
    payload = {
        "comment": \"\".join(texts),
        "languages": ["en"]
    }
    # Unimplemented stub: replace with actual API call if needed
    # response = requests.post(f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze", json=payload, headers={"key": os.getenv("PERSPECTIVE_API_KEY")})
    # Assume safety check returns a simple result
    clean = all(not any(bad in txt.lower() for bad in ["error", "fail", "exception"]) for txt in texts)
    return {
        "clean": clean,
        "detected": None if clean else [\"potential unsafe content detected\"]
    }