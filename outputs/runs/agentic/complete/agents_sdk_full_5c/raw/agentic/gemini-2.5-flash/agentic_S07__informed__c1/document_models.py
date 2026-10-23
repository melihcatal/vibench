# This file can be used to define local request, response, or normalization helpers.
# For Google Document AI, the SDK models are often sufficient.

# Example of a simple Pydantic-like model for extracted text
class ExtractedText:
    def __init__(self, text: str, confidence: float = None):
        self.text = text
        self.confidence = confidence

    def to_dict(self):
        return {"text": self.text, "confidence": self.confidence}

# Example of a simple Pydantic-like model for a key-value pair
class KeyValuePair:
    def __init__(self, key: str, value: str, key_confidence: float = None, value_confidence: float = None):
        self.key = key
        self.value = value
        self.key_confidence = key_confidence
        self.value_confidence = value_confidence

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "key_confidence": self.key_confidence,
            "value_confidence": self.value_confidence,
        }

# This file could also contain functions to normalize Document AI output
# into these custom models if desired.
