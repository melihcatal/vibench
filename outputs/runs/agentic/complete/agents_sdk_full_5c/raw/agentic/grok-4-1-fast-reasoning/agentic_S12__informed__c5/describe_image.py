from vision_client import get_azure_vision_client, load_image_bytes
from vision_models import ImageCaption
from azure.ai.vision.imageanalysis.models import ImageAnalysisFeature

def describe_image(image_path: str) -> ImageCaption:
    client = get_azure_vision_client()
    image_bytes = load_image_bytes(image_path)
    result = client.analyze(
        image_bytes=image_bytes,
        features=[ImageAnalysisFeature.CAPTION]
    )
    caption_result = result.caption_result
    return {
        "caption": caption_result.caption,
        "confidence": caption_result.confidence
    }