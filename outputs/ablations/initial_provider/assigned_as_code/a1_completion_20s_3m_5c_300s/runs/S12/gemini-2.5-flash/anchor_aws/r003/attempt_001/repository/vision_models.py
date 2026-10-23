class ImagePayload:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes


class Label:
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence


class LabelDetectionResult:
    def __init__(self, labels: list[Label]):
        self.labels = labels
