from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from google.cloud import vision


@dataclass
class LabelDetectionResult:
    labels: List[Dict[str, Any]]

    @classmethod
    def from_google_vision(
        cls, response: vision.AnnotateImageResponse
    ) -> "LabelDetectionResult":
        labels = []
        for label in response.label_annotations:
            labels.append(
                {
                    "description": label.description,
                    "score": label.score,
                    "mid": label.mid,
                    "topicality": label.topicality,
                }
            )
        return cls(labels=labels)


@dataclass
class ImageDescriptionResult:
    description: str
    captions: List[Dict[str, Any]]

    @classmethod
    def from_google_vision(
        cls, response: vision.AnnotateImageResponse
    ) -> "ImageDescriptionResult":
        captions = []
        description_parts = []

        for label in response.label_annotations:
            if label.score > 0.7:
                description_parts.append(label.description)

        for obj in response.localized_object_annotations:
            captions.append(
                {
                    "name": obj.name,
                    "score": obj.score,
                    "bounding_poly": [
                        (vertex.x, vertex.y)
                        for vertex in obj.bounding_poly.normalized_vertices
                    ],
                }
            )

        description = ", ".join(description_parts[:5])
        return cls(description=description, captions=captions)


@dataclass
class TextDetectionResult:
    texts: List[Dict[str, Any]]
    full_text: Optional[str]

    @classmethod
    def from_google_vision(
        cls, response: vision.AnnotateImageResponse
    ) -> "TextDetectionResult":
        texts = []
        full_text = None

        if response.full_text_annotation:
            full_text = response.full_text_annotation.text

        for text in response.text_annotations:
            texts.append(
                {
                    "description": text.description,
                    "bounding_poly": [
                        (vertex.x, vertex.y) for vertex in text.bounding_poly.vertices
                    ],
                }
            )

        return cls(texts=texts, full_text=full_text)


@dataclass
class SafetyScoreResult:
    safe_search_annotation: Dict[str, Any]
    is_safe: bool

    @classmethod
    def from_google_vision(
        cls, response: vision.AnnotateImageResponse
    ) -> "SafetyScoreResult":
        safe_search = response.safe_search_annotation
        annotation_dict = {
            "adult": safe_search.adult.name,
            "spoof": safe_search.spoof.name,
            "medical": safe_search.medical.name,
            "violence": safe_search.violence.name,
            "racy": safe_search.racy.name,
        }

        is_safe = (
            safe_search.adult <= vision.Likelihood.POSSIBLE
            and safe_search.violence <= vision.Likelihood.POSSIBLE
            and safe_search.racy <= vision.Likelihood.POSSIBLE
        )

        return cls(safe_search_annotation=annotation_dict, is_safe=is_safe)
