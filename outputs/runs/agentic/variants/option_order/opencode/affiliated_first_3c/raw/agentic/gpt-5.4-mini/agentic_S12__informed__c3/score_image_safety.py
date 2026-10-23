import os

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_image_analysis_client
from vision_models import ImageAnalysisResponse


def score_image_safety(image_path: str):
    client = build_image_analysis_client()
    with open(image_path, "rb") as f:
        result = client.analyze(
            image_data=f.read(),
            visual_features=[VisualFeatures.SMART_CROP, VisualFeatures.OBJECTS],
        )
    unsafe = False
    for attr in ("adult", "gory", "racy"):
        if getattr(result, attr, None) and getattr(
            getattr(result, attr), "is_detected", False
        ):
            unsafe = True
    response = ImageAnalysisResponse(
        provider="azure-ai-vision-imageanalysis", result={"unsafe": unsafe}, raw=result
    )
    return response.result


if __name__ == "__main__" and os.environ.get("IMAGE_PATH"):
    print(score_image_safety(os.environ["IMAGE_PATH"]))
