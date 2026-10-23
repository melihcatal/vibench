from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import get_azure_vision_client, load_image_input
from vision_models import TextDetectionResult, normalize_strings


def detect_image_text(
    image_path: str, image_url: str | None = None
) -> TextDetectionResult:
    client = get_azure_vision_client()
    image = load_image_input(image_path, image_url)
    source = (
        {"image_url": image.image_url}
        if image.image_url
        else {"image_data": open(image.image_path, "rb").read()}
    )
    result = client.analyze(**source, visual_features=[VisualFeatures.READ])
    texts = []
    if getattr(result, "read", None) and getattr(result.read, "blocks", None):
        for block in result.read.blocks:
            for line in getattr(block, "lines", []):
                texts.append(line.text)
    return TextDetectionResult(
        texts=normalize_strings(texts),
        raw=result.as_dict() if hasattr(result, "as_dict") else {"result": str(result)},
    )


__all__ = ["detect_image_text"]
