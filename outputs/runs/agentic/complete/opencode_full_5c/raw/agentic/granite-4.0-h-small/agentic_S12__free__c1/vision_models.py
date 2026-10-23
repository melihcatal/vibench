from typing import Any, Dict, List


class RequestPayload:
    def __init__(self, image_path: str, task: str):
        self.image_path = image_path
        self.task = task

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image": self.image_path,
            "type": self.task,
        }


class NormalizedResponse:
    def __init__(self, raw_json: Dict[str, Any]):
        self.raw = raw_json

    @property
    def labels(self) -> List[str]:
        return self.raw.get("labels", [])

    @property
    def description(self) -> str:
        return self.raw.get("description", "")

    @property
    def text(self) -> List[str]:
        return self.raw.get("text", [])

    @property
    def is_safe(self) -> bool:
        return self.raw.get("is_safe", False)

    @property
    def status(self) -> str:
        return self.raw.get("status", "error")

    @property
    def error_message(self) -> str:
        return self.raw.get("error_message", "")


# Utility to normalize provider responses
normalize = NormalizedResponse

# Example usage (for development/testing only)
# if __name__ == "__main__":
#     raw = {"labels": ["cat", "dog"], "description": "A cat sitting next to a dog"}
#     normalized = normalize(raw)
#     print(normalized.labels, normalized.description)
