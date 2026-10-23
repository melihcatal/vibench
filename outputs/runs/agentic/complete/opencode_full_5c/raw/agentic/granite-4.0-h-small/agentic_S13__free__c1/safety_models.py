```python
# safety_models.py
# HELPER: Define local request, response, and normalization helpers for Text Content Safety

from typing import Dict, Any, List
from safety_client import get_client_config

class SafetyRequest:
    """Wrapper for building requests to the safety service."""
    def __init__(self, text: str, model_id: str = None):
        cfg = get_client_config()
        self.payload = {
            'text': text,
            'model': model_id or cfg['model_id']
        }
    def to_dict(self) -> Dict[str, Any]:
        return self.payload

class SafetyResponse:
    """Normalized response from the safety service."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        # Flatten scores into a simple dict {category: score}
        self.scores: Dict[str, float] = {}
        for cat, value in raw.get('categories', {}).items():
            # Assume provider may return nested dicts; normalize to float
            if isinstance(value, (int, float)):
                self.scores[cat] = float(value)
            elif isinstance(value, dict) and 'score' in value:
                self.scores[cat] = float(value['score'])
    def get_score(self, category: str) -> float:
        return self.scores.get(category, 0.0)
    def categories(self) -> List[str]:
        return list(self.scores.keys())
    def is_unsafe(self, thresholds: Dict[str, float]) -> bool:
        """Return True if any category exceeds its threshold."""
        for cat, thresh in thresholds.items():
            if self.get_score(cat) >= thresh:
                return True
        return False
```