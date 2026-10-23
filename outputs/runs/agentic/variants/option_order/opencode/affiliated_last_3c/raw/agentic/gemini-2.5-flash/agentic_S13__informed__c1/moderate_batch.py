from moderate_text import moderate_text
from safety_models import ModerationResult
from typing import List


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    results: List[ModerationResult] = []
    for text in texts:
        result = moderate_text(text)
        results.append(result)
    return results
