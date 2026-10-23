from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ImageRequest:
    """Represents an image for analysis."""
    image_bytes: Optional[bytes] = None
    image_uri: Optional[str] = None # e.g., gs://bucket/object or http://example.com/image.jpg

@dataclass
class LabelResult:
    """Detected label or object in an image."""
    description: str
    score: float

@dataclass
class TextResult:
    """Detected text in an image."""
    text: str
    bounds: List[Dict[str, Any]] = field(default_factory=list) # Bounding box coordinates

@dataclass
class SafeSearchResult:
    """Safety classification results for an image."""
    adult: str
    spoof: str
    medical: str
    violence: str
    racy: str

@dataclass
class ImageDescriptionResult:
    """A generated description for an image."""
    description: str
    confidence: Optional[float] = None

@dataclass
class TranslationResult:
    """Result of a text translation operation."""
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class TextSafetyResult:
    """Result of text safety analysis."""
    attribute_scores: Dict[str, float] # e.g., {"TOXICITY": 0.8, "SEVERE_TOXICITY": 0.5}

@dataclass
class ArchiveResult:
    """Result of archiving an asset."""
    asset_uri: str
    file_name: str
