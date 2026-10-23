import argparse
import json
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient, VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_client import image_to_bytes
from vision_models import ImageDescription
from azure.ai.vision.imageanalysis import ImageAnalysisResult

def describe_image(image_path: str) -> ImageDescription:
    endpoint = os.environ['AZURE_VISION_ENDPOINT']
    key = os.environ['AZURE_VISION_KEY']
    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = client.analyze(image_bytes=image_to_bytes(image_path), visual_features=[VisualFeatures.CAPTION])
    caption = result.caption
    desc = caption.content if caption else ''
    conf = caption.confidence.value if caption else 0.0
    return {'description': desc, 'confidence': conf}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Describe image using Azure AI Vision')
    parser.add_argument('image_path', help='Path to input image')
    args = parser.parse_args()
    result = describe_image(args.image_path)
    print(json.dumps(result, indent=2))