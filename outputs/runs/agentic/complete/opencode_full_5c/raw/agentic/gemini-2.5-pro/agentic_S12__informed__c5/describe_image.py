from vision_client import get_azure_vision_client
from vision_models import ImageDescription
from azure.ai.vision.imageanalysis.models import VisualFeatures


def describe_image(image_url: str) -> ImageDescription:
    client = get_azure_vision_client()

    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION],
    )

    if result.caption is not None:
        return ImageDescription(
            description=result.caption.text,
            confidence=result.caption.confidence,
        )
    return ImageDescription(description="", confidence=0.0)
