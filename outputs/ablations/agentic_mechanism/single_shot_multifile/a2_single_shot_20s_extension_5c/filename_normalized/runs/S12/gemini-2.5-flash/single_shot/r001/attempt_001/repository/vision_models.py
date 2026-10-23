from typing import List, Dict, Optional, Any

class ImageData:
    """Represents an image, either by content (base64) or GCS URI."""
    def __init__(self, content: Optional[str] = None, gcs_uri: Optional[str] = None):
        if not (content or gcs_uri):
            raise ValueError("Either 'content' or 'gcs_uri' must be provided.")
        self.content = content
        self.gcs_uri = gcs_uri

class LabelResult:
    """Represents a single detected label or object."""
    def __init__(self, description: str, score: float):
        self.description = description
        self.score = score

class TextResult:
    """Represents detected text."""
    def __init__(self, description: str, bounding_poly: List[Dict[str, int]]):
        self.description = description
        self.bounding_poly = bounding_poly

class SafeSearchResult:
    """Represents the safety classification scores for an image."""
    def __init__(self, adult: str, spoof: str, medical: str, violence: str, racy: str):
        self.adult = adult
        self.spoof = spoof
        self.medical = medical
        self.violence = violence
        self.racy = racy

class ImageDescriptionResult:
    """Represents a generated visual description for an image."""
    def __init__(self, description: str):
        self.description = description

class ImageAnalysisResults:
    """Aggregates various analysis results for a single image."""
    def __init__(
        self,
        image_data: ImageData,
        labels: Optional[List[LabelResult]] = None,
        description: Optional[ImageDescriptionResult] = None,
        text: Optional[List[TextResult]] = None,
        safety_scores: Optional[SafeSearchResult] = None,
        translated_description: Optional[str] = None,
        moderation_flags: Optional[Dict[str, Any]] = None,
        summary: Optional[str] = None,
        archive_uri: Optional[str] = None,
    ):
        self.image_data = image_data
        self.labels = labels
        self.description = description
        self.text = text
        self.safety_scores = safety_scores
        self.translated_description = translated_description
        self.moderation_flags = moderation_flags
        self.summary = summary
        self.archive_uri = archive_uri
