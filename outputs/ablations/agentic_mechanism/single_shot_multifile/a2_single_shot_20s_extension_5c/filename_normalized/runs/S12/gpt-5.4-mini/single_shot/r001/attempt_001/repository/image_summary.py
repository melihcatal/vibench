import json
from typing import Any, Dict, List

from vision_models import ImageDescriptionResponse, ImageLabelDetectionResponse, ImageSafetyResponse, ImageTextDetectionResponse


def summarize_visual_analysis(labels: ImageLabelDetectionResponse, description: ImageDescriptionResponse, text: ImageTextDetectionResponse, safety: ImageSafetyResponse) -> Dict[str, Any]:
    label_names = [item.name for item in labels.labels[:5]]
    summary = {
        "headline": description.description,
        "top_labels": label_names,
        "text_snippet": " ".join(text.text_lines[:3]),
        "is_safe": safety.safe,
        "safety_reasons": safety.reasons,
    }
    return summary


def serialize_visual_summary(summary: Dict[str, Any]) -> str:
    return json.dumps(summary, ensure_ascii=False)
