from typing import List, Dict


class VisionModels:
    @staticmethod
    def normalize_labels(labels: List[str]) -> Dict[str, float]:
        return {label: 1.0 for label in labels}

    @staticmethod
    def normalize_description(description: str) -> str:
        return description.strip()
