from typing import Dict, Any

class TextContentSafetyRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {'text': self.text}

class TextContentSafetyResponse:
    def __init__(self, is_safe: bool, safety_score: float):
        self.is_safe = is_safe
        self.safety_score = safety_score

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['is_safe'], data['safety_score'])

def normalize_safety_score(score: float) -> float:
    return max(0.0, min(1.0, score))