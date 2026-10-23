from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ImageAnalysisResult:
    image_uri: str
    labels: List[str]
    description: Optional[str]
    detected_text: List[str]
    safety_scores: Dict[str, str]

@dataclass
class SummaryResult:
    original_analysis: ImageAnalysisResult
    summary_text: str

@dataclass
class TranslatedDescriptionResult:
    original_description: str
    translated_description: str
    target_language: str

@dataclass
class TextSafetyResult:
    original_text: str
    safety_check_result: str

@dataclass
class ArchiveResult:
    image_uri: str
    archive_location: str
    metadata_location: str

# You can add utility functions for payload normalization or response parsing here
# For example, a function to convert Cloud Vision API Likelihood enum to string.

def likelihood_to_string(likelihood_enum) -> str:
    from google.cloud.vision_v1p3.types import Likelihood
    # Map the numeric likelihood value to its string name for easier interpretation.
    # LIKELIHOOD_UNSPECIFIED = 0
    # VERY_UNLIKELY = 1
    # UNLIKELY = 2
    # POSSIBLE = 3
    # LIKELY = 4
    # VERY_LIKELY = 5
    if likelihood_enum == Likelihood.VERY_UNLIKELY:
        return "VERY_UNLIKELY"
    elif likelihood_enum == Likelihood.UNLIKELY:
        return "UNLIKELY"
    elif likelihood_enum == Likelihood.POSSIBLE:
        return "POSSIBLE"
    elif likelihood_enum == Likelihood.LIKELY:
        return "LIKELY"
    elif likelihood_enum == Likelihood.VERY_LIKELY:
        return "VERY_LIKELY"
    else:
        return "UNKNOWN"

if __name__ == '__main__':
    # Example usage for demonstration
    result = ImageAnalysisResult(
        image_uri="gs://my-bucket/image.jpg",
        labels=["cat", "animal"],
        description="A cat sitting on a couch.",
        detected_text=["MEOW"],
        safety_scores={'adult': 'VERY_UNLIKELY'}
    )
    print(result)

    print("\nLikelihood to string example:")
    from google.cloud.vision_v1p3.types import Likelihood
    print(f"Likelihood.VERY_LIKELY: {likelihood_to_string(Likelihood.VERY_LIKELY)}")
    print(f"Likelihood.UNLIKELY: {likelihood_to_string(Likelihood.UNLIKELY)}")
