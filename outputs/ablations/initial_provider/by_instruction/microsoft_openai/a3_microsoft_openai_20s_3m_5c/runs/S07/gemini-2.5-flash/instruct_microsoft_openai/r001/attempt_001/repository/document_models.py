from typing import List, Dict, Any

class ExtractedText:
    def __init__(self, text: str, confidence: float = None):
        self.text = text
        self.confidence = confidence

    def to_dict(self):
        return {"text": self.text, "confidence": self.confidence}

class ExtractedBlock:
    def __init__(self, content: str, bounding_box: List[float], kind: str, confidence: float = None):
        self.content = content
        self.bounding_box = bounding_box
        self.kind = kind
        self.confidence = confidence

    def to_dict(self):
        return {"content": self.content, "bounding_box": self.bounding_box, "kind": self.kind, "confidence": self.confidence}

class ExtractedTable:
    def __init__(self, rows: List[List[Dict[str, Any]]], bounding_box: List[float], confidence: float = None):
        self.rows = rows
        self.bounding_box = bounding_box
        self.confidence = confidence

    def to_dict(self):
        return {"rows": self.rows, "bounding_box": self.bounding_box, "confidence": self.confidence}

class ExtractedKeyValuePair:
    def __init__(self, key: ExtractedText, value: ExtractedText, confidence: float = None):
        self.key = key
        self.value = value
        self.confidence = confidence

    def to_dict(self):
        return {"key": self.key.to_dict() if self.key else None, "value": self.value.to_dict() if self.value else None, "confidence": self.confidence}
