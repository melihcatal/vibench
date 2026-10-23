from typing import Dict, Optional

from safety_client import moderate_text
from safety_models import normalize_thresholds


def safety_threshold(text: str, thresholds: Optional[Dict[str, float]] = None) -> Dict[str, object]:
    decision = moderate_text(text, thresholds=normalize_thresholds(thresholds))
    return {"allowed": decision.allowed, "scores": decision.scores, "thresholds": normalize_thresholds(thresholds)}
