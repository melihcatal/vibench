from typing import List, Dict, Any, Optional

# Placeholder for potential shared models or utility functions
# In a more complex scenario, this might contain Pydantic models
# for request/response validation and normalization.

class ExtractedText:
    text: str
    language: Optional[str]

    def __init__(self, text: str, language: Optional[str] = None):
        self.text = text
        self.language = language

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "language": self.language}

class ExtractedTable:
    rows: List[List[str]]
    
    def __init__(self, rows: List[List[str]]):
        self.rows = rows

    def to_dict(self) -> Dict[str, Any]:
        return {"rows": self.rows}

class KeyValuePair:
    key: str
    value: str
    confidence: Optional[float]

    def __init__(self, key: str, value: str, confidence: Optional[float] = None):
        self.key = key
        self.value = value
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value, "confidence": self.confidence}

