from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_vision_client
from vision_models import normalize_detected_text, DetectedTextRegion


def detect_image_text(image_url: str) -> list[DetectedTextRegion]:
    client = get_vision_client()
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.READ],
    )
    raw_read = {"lines": []}
    if result.read is not None:
        for line in result.read.lines:
            bbox = None
            if line.bounding_polygon:
                coords = line.bounding_polygon
                bbox = {
                    "points": [
                        {"x": coords[0], "y": coords[1]},
                        {"x": coords[2], "y": coords[3]},
                        {"x": coords[4], "y": coords[5]},
                        {"x": coords[6], "y": coords[7]},
                    ]
                }
            raw_read["lines"].append(
                {
                    "text": line.text,
                    "confidence": line.confidence,
                    "bounding_box": bbox,
                }
            )
    text_regions = normalize_detected_text(raw_read)
    return text_regions
