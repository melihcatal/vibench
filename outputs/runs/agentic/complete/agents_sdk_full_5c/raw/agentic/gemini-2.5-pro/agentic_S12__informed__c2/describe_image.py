from vision_client import get_azure_vision_client
from vision_models import ImageDescription, DescriptionResponse
from azure.ai.vision.imageanalysis.models import VisualFeatures

def describe_image(image_url: str) -> DescriptionResponse:
    """
    Generates a human-readable caption for an image using Azure AI Vision.

    Args:
        image_url: The public URL of the image.

    Returns:
        A DescriptionResponse object containing the generated caption.
    """
    client = get_azure_vision_client()
    
    result = client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.CAPTION],
        gender_neutral_caption=True,
    )

    descriptions = []
    if result.caption is not None:
        descriptions.append(
            ImageDescription(
                caption=result.caption.text,
                confidence=result.caption.confidence
            )
        )

    return DescriptionResponse(descriptions=descriptions)
