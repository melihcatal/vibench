import base64
from azure.ai.contentsafety import AnalyzeImageOptions
from vision_client import get_azure_content_safety_client
from vision_models import parse_azure_content_safety_result

def score_image_safety(image_bytes: bytes):
    client = get_azure_content_safety_client()
    options = AnalyzeImageOptions(image={"content": image_bytes})
    result = client.analyze_image(options)
    return parse_azure_content_safety_result(result)
