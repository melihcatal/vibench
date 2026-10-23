from azure.ai.vision.imageanalysis import VisualFeatures
from vision_client import get_image_analysis_client
from vision_models import ImageAnalysisRequest, DescriptionResult

def describe_image(payload: ImageAnalysisRequest):
    client = get_image_analysis_client()
    result = client.analyze(image_data=payload.image_bytes, visual_features=[VisualFeatures.DENSE_CAPTION])

    description = None
    if result.dense_captions.list:
        # Azure Vision often returns multiple captions, pick the most confident one for overall description
        best_caption = sorted(result.dense_captions.list, key=lambda x: x.confidence, reverse=True)[0]
        description = DescriptionResult(text=best_caption.text, confidence=best_caption.confidence)

    return {"description": description}
