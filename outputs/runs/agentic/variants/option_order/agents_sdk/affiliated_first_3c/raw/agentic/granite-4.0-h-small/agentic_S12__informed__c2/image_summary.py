# image_summary.py
from typing import List, Dict
from vision_models import ImageLabelsResponse, ImageDescriptionResponse, SafetyCheckResponse

def summarize_visual_analysis(labels: ImageLabelsResponse,
                                description: ImageDescriptionResponse,
                                safety: SafetyCheckResponse) -> Dict[str, any]:
    summary = {
        'labels': labels.labels,
        'description': description.descriptions[0] if description.descriptions else None,
        'safety': safety.safety_results
    }
    return summary
