from vision_models import LabelDetectionResponse, ImageDescriptionResponse, TextDetectionResponse, SafetyDetectionResponse

def summarize_image_analysis(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    text_detection: TextDetectionResponse,
    safety_scores: SafetyDetectionResponse
) -> dict:
    summary = {
        "labels": [label['name'] for label in labels.labels],
        "description": description.description,
        "detected_text": text_detection.text,
        "safety_annotations": safety_scores.safe_search_annotations
    }
    return summary
