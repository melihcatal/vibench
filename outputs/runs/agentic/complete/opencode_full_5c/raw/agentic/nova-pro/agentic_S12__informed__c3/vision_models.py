from typing import List, Dict


class VisionResponse:
    def __init__(
        self, labels: List[str], description: str, texts: List[str], safety: Dict
    ):
        self.labels = labels
        self.description = description
        self.texts = texts
        self.safety = safety
