import os

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_image_analysis_client
from vision_models import ImageAnalysisResponse


def describe_image(image_path: str):
    client = build_image_analysis_client()
    with open(image_path, "rb") as f:
        result = client.analyze(
            image_data=f.read(), visual_features=[VisualFeatures.CAPTION]
        )
    caption = getattr(getattr(result, "caption", None), "text", "")
    response = ImageAnalysisResponse(
        provider="azure-ai-vision-imageanalysis", result=caption, raw=result
    )
    return response.result


if __name__ == "__main__" and os.environ.get("IMAGE_PATH"):
    print(describe_image(os.environ["IMAGE_PATH"]))
