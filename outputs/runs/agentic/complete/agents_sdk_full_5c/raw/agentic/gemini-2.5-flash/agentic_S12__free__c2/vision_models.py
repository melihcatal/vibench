from typing import Dict, List, Any

class ImageAnalysisRequest:
    """Represents a request for image analysis."""
    def __init__(self, image_bytes: bytes, image_id: str = None):
        self.image_bytes = image_bytes
        self.image_id = image_id

class ImageAnalysisResult:
    """Aggregates results from various image analysis tasks."""
    def __init__(self, image_id: str = None):
        self.image_id = image_id
        self.labels: List[str] = []
        self.description: str = ""
        self.detected_text: str = ""
        self.safety_scores: Dict[str, str] = {}
        self.summary: str = ""
        self.translated_description: Dict[str, str] = {} # lang_code -> translated_text
        self.text_safety_check: Dict[str, Any] = {} # Results from text safety
        self.archive_url: str = ""
