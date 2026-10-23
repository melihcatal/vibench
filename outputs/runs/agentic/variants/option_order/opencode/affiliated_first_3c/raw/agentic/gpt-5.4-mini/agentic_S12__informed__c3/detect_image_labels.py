import os

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_image_analysis_client, read_image_bytes
from vision_models import ImageAnalysisRequest, ImageAnalysisResponse, join_text


def detect_image_labels(image_path: str):
    request = ImageAnalysisRequest(image_path=image_path)
    client = build_image_analysis_client()
    with open(request.image_path, "rb") as f:
        result = client.analyze(
            image_data=f.read(),
            visual_features=[VisualFeatures.OBJECTS, VisualFeatures.TAGS],
        )
    labels = []
    if getattr(result, "objects", None):
        labels.extend(
            [
                getattr(obj, "tags", [getattr(obj, "name", "")])[0]
                for obj in result.objects
            ]
        )
    if getattr(result, "tags", None):
        labels.extend([tag.name for tag in result.tags])
    response = ImageAnalysisResponse(
        provider="azure-ai-vision-imageanalysis", result=join_text(labels), raw=result
    )
    return response.result


if __name__ == "__main__" and os.environ.get("IMAGE_PATH"):
    print(detect_image_labels(os.environ["IMAGE_PATH"]))
