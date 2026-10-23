import json
from vision_models import NormalizedResponse


class ImageSummary:
    def __init__(
        self, labels: List[str], description: str, text: List[str], safe: bool
    ):
        self.labels = labels
        self.description = description
        self.text = text
        self.safe = safe

    def as_dict(self) -> dict:
        return {
            "labels": self.labels,
            "description": self.description,
            "text_fragments": self.text,
            "safe": self.safe,
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2)


if __name__ == "__main__":
    # Example aggregation (replace with real provider data when available)
    labels = ["cat", "tree"]
    description = "A cat sitting under a tree."
    text = []
    safety = True
    summary = ImageSummary(labels, description, text, safety)
    print(summary.to_json())
