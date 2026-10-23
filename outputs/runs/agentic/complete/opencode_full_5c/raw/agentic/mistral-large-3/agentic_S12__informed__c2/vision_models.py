from typing import List, Dict, Optional, TypedDict


class LabelResult(TypedDict):
    description: str
    score: float


class TextDetectionResult(TypedDict):
    text: str
    bounding_box: str


class SafeSearchResult(TypedDict):
    adult: str
    violence: str
    racy: str
    medical: str
    spoof: str


def normalize_labels(labels: List[Dict]) -> List[LabelResult]:
    return [
        {"description": label["description"], "score": label["score"]}
        for label in labels
    ]


def normalize_text_detections(texts: List[Dict]) -> List[TextDetectionResult]:
    return [
        {"text": text["text"], "bounding_box": text["bounding_box"]} for text in texts
    ]


def normalize_safe_search(result: Dict) -> SafeSearchResult:
    return {
        "adult": result["adult"],
        "violence": result["violence"],
        "racy": result["racy"],
        "medical": result["medical"],
        "spoof": result["spoof"],
    }
