from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import get_azure_vision_client, load_image_input
from vision_models import SafetyResult, normalize_strings


def score_image_safety(image_path: str, image_url: str | None = None) -> SafetyResult:
    client = get_azure_vision_client()
    image = load_image_input(image_path, image_url)
    source = (
        {"image_url": image.image_url}
        if image.image_url
        else {"image_data": open(image.image_path, "rb").read()}
    )
    result = client.analyze(
        **source, visual_features=[VisualFeatures.OBJECTS, VisualFeatures.TAGS]
    )
    categories = []
    unsafe = False
    for tag in getattr(result, "tags", []) or []:
        name = getattr(tag, "name", "")
        if name:
            categories.append(name)
            if name.lower() in {"adult", "racy", "violence", "gore"}:
                unsafe = True
    return SafetyResult(
        unsafe=unsafe,
        categories=normalize_strings(categories),
        raw=result.as_dict() if hasattr(result, "as_dict") else {"result": str(result)},
    )


__all__ = ["score_image_safety"]
