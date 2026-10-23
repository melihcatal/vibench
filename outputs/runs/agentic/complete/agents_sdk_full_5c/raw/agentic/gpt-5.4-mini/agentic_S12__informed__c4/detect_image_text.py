from vision_client import feature_set_for_text, get_client, image_source_from_base64, image_source_from_path
from vision_models import ImageInput, ImageAnalysisResult, normalize_text


def detect_image_text(image: ImageInput) -> ImageAnalysisResult:
    image.validate()
    client = get_client()
    payload = image_source_from_path(image.image_path) if image.image_path else image_source_from_base64(image.image_b64)
    result = client.analyze(image_data=payload, visual_features=feature_set_for_text())
    return ImageAnalysisResult(text=normalize_text(result))
