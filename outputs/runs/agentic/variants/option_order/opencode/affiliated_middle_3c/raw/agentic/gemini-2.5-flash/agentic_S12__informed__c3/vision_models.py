import base64
from typing import List, Dict, Any


class ImageRequest:
    def __init__(self, image_content: bytes = None, image_uri: str = None):
        self.image_content = image_content
        self.image_uri = image_uri

    def to_vision_image(self):
        if self.image_content:
            return {"content": base64.b64encode(self.image_content).decode("utf-8")}
        elif self.image_uri:
            return {"source": {"image_uri": self.image_uri}}
        return {}


class LabelDetectionResponse:
    def __init__(self, labels: List[str]):
        self.labels = labels

    @classmethod
    def from_vision_response(cls, response: Dict[str, Any]):
        labels = [label.description for label in response.label_annotations]
        return cls(labels)


class TextDetectionResponse:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_vision_response(cls, response: Dict[str, Any]):
        text = (
            response.full_text_annotation.text if response.full_text_annotation else ""
        )
        return cls(text)


class SafeSearchDetectionResponse:
    def __init__(self, adult: str, spoof: str, medical: str, violence: str, racy: str):
        self.adult = adult
        self.spoof = spoof
        self.medical = medical
        self.violence = violence
        self.racy = racy

    @classmethod
    def from_vision_response(cls, response: Dict[str, Any]):
        safe_search = response.safe_search_annotation
        return cls(
            adult=safe_search.adult.name
            if safe_search and safe_search.adult
            else "UNKNOWN",
            spoof=safe_search.spoof.name
            if safe_search and safe_search.spoof
            else "UNKNOWN",
            medical=safe_search.medical.name
            if safe_search and safe_search.medical
            else "UNKNOWN",
            violence=safe_search.violence.name
            if safe_search and safe_search.violence
            else "UNKNOWN",
            racy=safe_search.racy.name
            if safe_search and safe_search.racy
            else "UNKNOWN",
        )


class ImageDescriptionResponse:
    def __init__(self, description: str):
        self.description = description

    @classmethod
    def from_vision_response(cls, response: Dict[str, Any]):
        # Google Cloud Vision doesn't have a direct 'describe image' feature like some LLMs.
        # We'll approximate it by joining labels or using web entities if available.
        if response.label_annotations:
            description = ", ".join(
                [label.description for label in response.label_annotations]
            )
        elif response.web_detection and response.web_detection.best_guess_labels:
            description = response.web_detection.best_guess_labels[0].label
        else:
            description = "No clear description available."
        return cls(description)
