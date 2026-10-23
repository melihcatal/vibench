# safety_threshold.py
import json
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def apply_thresholds(response: ModerationResponse, thresholds: dict) -> bool:
    """Apply per‑category thresholds to decide whether to allow the text.

    Uses Amazon Comprehend Toxicity as the concrete provider.
    """
    allowed = True
    for cat, limit in thresholds.items():
        if cat in response.scores:
            if response.scores[cat] > limit:
                allowed = False
                break
    return allowed

if __name__ == "__main__":
    txt = "You are an idiot."
    client = SafetyClient()
    req = ModerationRequest(text=txt, language=client.detect_language(txt))
    resp = client.detect_toxicity(req)
    thresholds = {"toxicity": 0.2, "profanity": 0.3}
    print(json.dumps({
        "text": txt,
        "thresholds": thresholds,
        "allowed": apply_thresholds(resp, thresholds)
    }, indent=2))
