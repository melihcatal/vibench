from vision_models import VisionResponse
from detect_image_labels import detect_labels
from describe_image import describe_image
from detect_image_text import detect_text
from score_image_safety import check_safety


def summarize_visual_analysis(image_path):
    labels = detect_labels(image_path)
    description = describe_image(image_path)
    text = detect_text(image_path)
    safety = check_safety(image_path)
    return VisionResponse(
        {"labels": labels, "description": description, "text": text, "safety": safety}
    )
