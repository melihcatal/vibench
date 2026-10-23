from vision_client import feature_set_for_safety, get_client, image_source_from_base64, image_source_from_path
from vision_models import ImageInput, ImageAnalysisResult, normalize_safety_from_labels


def score_image_safety(image: ImageInput) -> ImageAnalysisResult:
    image.validate()
    client = get_client()
    payload = image_source_from_path(image.image_path) if image.image_path else image_source_from_base64(image.image_b64)
    result = client.analyze(image_data=payload, visual_features=feature_set_for_safety())
    return ImageAnalysisResult(safety=normalize_safety_from_labels(result))
