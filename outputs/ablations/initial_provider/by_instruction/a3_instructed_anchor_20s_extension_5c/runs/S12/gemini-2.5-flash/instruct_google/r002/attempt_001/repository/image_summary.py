from detect_image_labels import detect_image_labels
from describe_image import describe_image
from detect_image_text import detect_image_text
from score_image_safety import score_image_safety

# Provider-specific import for identification, even if not directly used in summary logic
from google.cloud import vision
# Could also include other Google Cloud client imports if they were used for downstream steps

def summarize_image_analysis(image_path):
    labels = detect_image_labels(image_path)
    description = describe_image(image_path)
    text_content = detect_image_text(image_path)
    safety_scores = score_image_safety(image_path)

    summary = {
        "image_path": image_path,
        "detected_labels": labels,
        "visual_description": description,
        "detected_text": text_content,
        "safety_scores": safety_scores,
    }
    return summary
