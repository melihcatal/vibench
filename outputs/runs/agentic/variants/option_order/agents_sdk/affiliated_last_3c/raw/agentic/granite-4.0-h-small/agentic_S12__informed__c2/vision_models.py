from dataclasses import dataclass
from typing import List, Dict

@dataclass
class LabelResult:
    categories: List[str] = None
    tags: List[str] = None
    descriptions: List[str] = None
    faces: List[dict] = None

    @classmethod
    def from_azure(cls, azure_result: dict):
        return cls(
            categories=azure_result.get("categories", []),
            tags=azure_result.get("tags", []),
            descriptions=azure_result.get("description", {}).get("captions", []),
            faces=azure_result.get("faces", [])
        )

@dataclass
class DescriptionResult:
    captions: List[str] = None

    @classmethod
    def from_azure(cls, azure_result: dict):
        return cls(
            captions=azure_result.get("description", {}).get("captions", [])
        )

@dataclass
class TextDetectionResult:
    text_detections: List[str] = None

    @classmethod
    def from_azure(cls, azure_result: dict):
        # Azure returns a collection of recognized lines/words
        lines = azure_result.get("recognitionResult", {}).get("lines", [])
        texts = [line["text"] for line in lines]
        return cls(text_detections=to_texts)

@dataclass
class SafetyResult:
    categories: Dict[str, str] = None
    detected: List[str] = None

    @classmethod
    def from_azure(cls, azure_result: dict):
        # Azure Content Safety returns a list of categories and findings
        categories = azure_result.get("categories", [])
        findings = azure_result.get("findings", [])
        return cls(categories=categories, detected=[f["category"] for f in findings])
