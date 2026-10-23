import base64
from azure.ai.vision.imageanalysis import ImageAnalysisOptions, VisualFeatures, ImageSource
from vision_client import get_azure_vision_client
from vision_models import prepare_image_for_azure_vision, parse_azure_caption_result

def describe_image(image_bytes: bytes):
    client = get_azure_vision_client()
    vision_source = ImageSource(image_bytes=prepare_image_for_azure_vision(image_bytes))
    analysis_options = ImageAnalysisOptions(
        visual_features=[VisualFeatures.CAPTION],
        language="en"
    )
    result = client.analyze(
        image_source=vision_source,
        analysis_options=analysis_options
    )
    return parse_azure_caption_result(result)
