# Moderates a batch of user messages and returns per-message decisions
from typing import List
from concurrent.futures import ThreadPoolExecutor
from moderate_text import moderate_text
from safety_models import SafetyDecision


def moderate_batch(texts: List[str], max_workers: int = 5) -> List[SafetyDecision]:
    """Moderate a batch of texts using Google Perspective API."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        decisions = list(executor.map(moderate_text, texts))
    return decisions