from azure.ai.vision.imageanalysis.models import VisualFeatures
from vision_client import get_vision_client
from vision_models import normalize_labels, ImageLabel, VisualAnalysisResult


def detect_image_labels(image_url: str) -> list[ImageLabel]:
    client = get_vision_client()
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS],
    )
    raw_tags = []
    if result.tags is not None:
        for tag in result.tags.list:
            raw_tags.append({"name": tag.name, "confidence": tag.confidence})
    raw_objects = []
    if result.objects is not None:
        for obj in result.objects.list:
            bbox = None
            if obj.bounding_box:
                bbox = {
                    "x": obj.bounding_box.x,
                    "y": obj.bounding_box.y,
                    "w": obj.bounding_box.w,
                    "h": obj.bounding_box.h,
                }
            raw_objects.append(
                {
                    "name": obj.name,
                    "confidence": obj.confidence,
                    "bounding_box": bbox,
                }
            )
    labels = normalize_labels(raw_tags)
    return labels


def detect_image_labels_full(image_url: str) -> VisualAnalysisResult:
    client = get_vision_client()
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS],
    )
    raw_tags = []
    if result.tags is not None:
        for tag in result.tags.list:
            raw_tags.append({"name": tag.name, "confidence": tag.confidence})
    raw_objects = []
    if result.objects is not None:
        for obj in result.objects.list:
            bbox = None
            if obj.bounding_box:
                bbox = {
                    "x": obj.bounding_box.x,
                    "y": obj.bounding_box.y,
                    "w": obj.bounding_box.w,
                    "h": obj.bounding_box.h,
                }
            raw_objects.append(
                {
                    "name": obj.name,
                    "confidence": obj.confidence,
                    "bounding_box": bbox,
                }
            )
    analysis = VisualAnalysisResult()
    analysis.labels = normalize_labels(raw_tags)
    from vision_models import normalize_objects

    analysis.objects = normalize_objects(raw_objects)
    return analysis
