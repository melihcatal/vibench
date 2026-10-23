from typing import Dict, Any
from vision_models import VisualAnalysisSummary, LabelDetectionResponse, ImageDescriptionResponse, TextDetectionResponse, ImageSafetyResponse

def image_summary(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    text: TextDetectionResponse,
    safety: ImageSafetyResponse
) -> Dict[str, Any]:
    """Summarizes visual analysis results into a structured report."""
    summary = VisualAnalysisSummary(
        labels=labels,
        description=description,
        text=text,
        safety=safety
    )
    
    return summary.dict()