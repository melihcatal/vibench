from vision_client import get_azure_vision_client
from vision_models import ImageDescription
from azure.ai.vision.imageanalysis.models import VisualFeatures


def describe_image(image_bytes: bytes) -> ImageDescription:
    client = get_azure_vision_client()
    result = client.analyze(
        image_data=image_bytes, visual_features=[VisualFeatures.CAPTION]
    )

    if result.caption is not None:
        return ImageDescription(
            text=result.caption.text, confidence=result.caption.confidence
        )
    return ImageDescription(text="", confidence=0.0)
