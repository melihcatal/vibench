from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    """Safety categories for image content."""

    ADULT = "adult"
    RACY = "racy"
    GORY = "gory"
    VIOLENT = "violent"
    HARMFUL = "harmful"


@dataclass
class LabelDetection:
    """Represents a detected label in an image."""

    description: str
    score: float
    provider: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class TextDetection:
    """Represents detected text in an image."""

    text: str
    confidence: float
    bounding_box: Optional[Dict[str, float]] = None
    provider: str = ""


@dataclass
class ImageDescription:
    """Represents a generated image description."""

    description: str
    model: str
    provider: str
    usage: Optional[Dict[str, int]] = None


@dataclass
class SafetyScore:
    """Represents safety scores for image content."""

    categories: Dict[SafetyCategory, float]
    is_safe: bool
    provider: str
    threshold: float = 0.5


class VisionResponseNormalizer:
    """Helper class for normalizing responses from different vision providers."""

    @staticmethod
    def normalize_google_labels(response) -> List[LabelDetection]:
        """Normalize Google Cloud Vision label detection response."""
        labels = []
        for label in response.label_annotations:
            labels.append(
                LabelDetection(
                    description=label.description,
                    score=label.score,
                    provider="google-cloud-vision",
                    metadata={"mid": label.mid, "topicality": label.topicality},
                )
            )
        return labels

    @staticmethod
    def normalize_aws_text(response) -> List[TextDetection]:
        """Normalize AWS Rekognition text detection response."""
        text_items = []
        for detection in response.get("TextDetections", []):
            if detection["Type"] == "LINE":
                text_items.append(
                    TextDetection(
                        text=detection["DetectedText"],
                        confidence=detection["Confidence"],
                        bounding_box=detection.get("Geometry", {}).get(
                            "BoundingBox", {}
                        ),
                        provider="aws-rekognition",
                    )
                )
        return text_items

    @staticmethod
    def normalize_openai_description(response) -> ImageDescription:
        """Normalize OpenAI image description response."""
        return ImageDescription(
            description=response["choices"][0]["message"]["content"].strip(),
            model=response["model"],
            provider="openai",
            usage=response.get("usage", {}),
        )

    @staticmethod
    def normalize_azure_safety(response) -> SafetyScore:
        """Normalize Azure Computer Vision safety analysis response."""
        adult_info = response.get("adult", {})
        categories = {
            SafetyCategory.ADULT: adult_info.get("adultScore", 0.0),
            SafetyCategory.RACY: adult_info.get("racyScore", 0.0),
            SafetyCategory.GORY: adult_info.get("goreScore", 0.0),
        }

        is_safe = not (
            adult_info.get("isAdultContent", False)
            or adult_info.get("isRacyContent", False)
            or adult_info.get("isGoryContent", False)
        )

        return SafetyScore(
            categories=categories, is_safe=is_safe, provider="azure-computer-vision"
        )


class VisionRequestBuilder:
    """Helper class for building requests for different vision providers."""

    @staticmethod
    def build_openai_vision_request(
        image_base64: str, prompt: str = "Describe this image."
    ) -> Dict[str, Any]:
        """Build request for OpenAI GPT-4 Vision."""
        return {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 150,
        }

    @staticmethod
    def build_azure_analysis_request() -> Dict[str, str]:
        """Build parameters for Azure Computer Vision analysis."""
        return {"visualFeatures": "Adult", "language": "en"}
