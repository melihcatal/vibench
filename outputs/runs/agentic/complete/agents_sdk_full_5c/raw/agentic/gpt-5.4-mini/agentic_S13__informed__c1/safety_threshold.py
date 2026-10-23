from typing import Dict

from safety_client import build_client
from safety_models import ModerationDecision, ModerationRequest, ThresholdRule


def safety_threshold(request: ModerationRequest, rules: Dict[str, float]) -> ModerationDecision:
    client = build_client()
    payload = {"text": request.text, "categories": list(rules.keys())}
    data = client.post("/contentsafety/text:analyze", payload)
    scores = {k: float(v) for k, v in data.get("categoryScores", {}).items()}
    violations = [category for category, threshold in rules.items() if scores.get(category, 0.0) > threshold]
    return ModerationDecision(allowed=not violations, category_scores=scores, reasons=violations)
