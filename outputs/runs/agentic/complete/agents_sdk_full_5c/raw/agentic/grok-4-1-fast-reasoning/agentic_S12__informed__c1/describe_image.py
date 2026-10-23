"""[SAME-SCENARIO] generates a short visual description for an image"""
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient, ImageAnalysisFeature
from vision_client import image_to_bytes, get_api_key
from vision_models import DescriptionResponse

def describe_image(image_path: str) -> DescriptionResponse:
    # Azure AI Vision
    endpoint = get_api_key('AZURE_VISION_ENDPOINT')
    key = get_api_key('AZURE_VISION_KEY')
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    content = image_to_bytes(image_path)
    poller = client.analyze(image_url=content, visual_features=[ImageAnalysisFeature.CAPTION])
    result = poller.result(timeout=30.0)
    return {'description': result.caption.description}
