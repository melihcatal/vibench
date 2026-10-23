from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import get_azure_vision_client, load_image_input
from vision_models import DescriptionResult


def describe_image(image_path: str, image_url: str | None = None) -> DescriptionResult:
    client = get_azure_vision_client()
    image = load_image_input(image_path, image_url)
    source = (
        {"image_url": image.image_url}
        if image.image_url
        else {"image_data": open(image.image_path, "rb").read()}
    )
    result = client.analyze(**source, visual_features=[VisualFeatures.CAPTION])
    description = getattr(getattr(result, "caption", None), "text", "")
    return DescriptionResult(
        description=description,
        raw=result.as_dict() if hasattr(result, "as_dict") else {"result": str(result)},
    )


__all__ = ["describe_image"]
