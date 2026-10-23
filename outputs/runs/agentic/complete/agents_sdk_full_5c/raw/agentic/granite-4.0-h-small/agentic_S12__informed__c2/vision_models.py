import dataclasses

class Label:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence
    
@dataclasses.dataclass
class Caption:
    text: str
    confidence: float = 0.0
    
@dataclasses.dataclass
class SafetyResult:
    safety_score: float  # 0.0 = unsafe, 1.0 = safe
