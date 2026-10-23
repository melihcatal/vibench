import os

from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_client import build_image_analysis_client
from vision_models import ImageAnalysisResponse, join_text


def detect_image_text(image_path: str):
    client = build_image_analysis_client()
    with open(image_path, "rb") as f:
        result = client.analyze(
            image_data=f.read(), visual_features=[VisualFeatures.READ]
        )
    lines = []
    read_result = getattr(result, "read", None)
    if read_result and getattr(read_result, "blocks", None):
        for block in read_result.blocks:
            for line in getattr(block, "lines", []):
                lines.append(getattr(line, "text", ""))
    response = ImageAnalysisResponse(
        provider="azure-ai-vision-imageanalysis", result=join_text(lines), raw=result
    )
    return response.result


if __name__ == "__main__" and os.environ.get("IMAGE_PATH"):
    print(detect_image_text(os.environ["IMAGE_PATH"]))
