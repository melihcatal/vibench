from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ImageDetectionRequest:
    image_uri: str


@dataclass
class LabelDetectionResponse:
    labels: List[str] = field(default_factory=list)


@dataclass
class TextDetectionResponse:
    text: str = ""


@dataclass
class SafeSearchDetectionResponse:
    adult: str = "UNKNOWN"
    spoof: str = "UNKNOWN"
    medical: str = "UNKNOWN"
    violence: str = "UNKNOWN"
    racy: str = "UNKNOWN"


@dataclass
class ImageDescriptionResponse:
    description: str = ""
    tags: List[str] = field(default_factory=list)


def normalize_label_detection_response(response: Any) -> LabelDetectionResponse:
    labels = [label.description for label in response.label_annotations]
    return LabelDetectionResponse(labels=labels)


def normalize_text_detection_response(response: Any) -> TextDetectionResponse:
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    return TextDetectionResponse(text=text)


def normalize_safe_search_detection_response(
    response: Any,
) -> SafeSearchDetectionResponse:
    safe_search = response.safe_search_annotation
    return SafeSearchDetectionResponse(
        adult=safe_search.adult.name,
        spoof=safe_search.spoof.name,
        medical=safe_search.medical.name,
        violence=safe_search.violence.name,
        racy=safe_search.racy.name,
    )


def normalize_image_description_response(response: Any) -> ImageDescriptionResponse:
    if response.text_annotations:
        description = response.text_annotations[0].description
        tags = [tag.description for tag in response.label_annotations]
        return ImageDescriptionResponse(description=description, tags=tags)
    return ImageDescriptionResponse()
