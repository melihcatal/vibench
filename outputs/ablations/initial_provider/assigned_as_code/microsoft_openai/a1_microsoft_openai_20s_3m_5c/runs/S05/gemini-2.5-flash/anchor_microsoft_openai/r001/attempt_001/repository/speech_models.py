# This file can be used for request/response normalization or custom data models
# For now, it remains largely empty as the Azure SDK handles much of this internally.
# It can be extended if specific application-level models or transformations are needed.

class StreamingRecognitionResult:
    def __init__(self, text, is_final):
        self.text = text
        self.is_final = is_final

    def to_dict(self):
        return {"text": self.text, "is_final": self.is_final}
