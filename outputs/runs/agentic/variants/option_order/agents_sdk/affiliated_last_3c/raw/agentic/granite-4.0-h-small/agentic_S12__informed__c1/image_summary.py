import os
import boto3
from vision_models import normalize_labels, normalize_description, normalize_text, normalize_safety
from vision_client import VisionClient
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.hlp.data.assets import AssetManagementClient

# Configure WatsonX
api_key = os.getenv('WATSONX_API_KEY')
project_id = os.getenv('WATSONX_PROJECT_ID')
watson_api = APIClient(api_key=api_key, project_id=project_id)
asset_mgmt = AssetManagementClient(api_key=api_key, project_id=project_id)

# Amazon Rekognition client for label detection
rekognition = boto3.client('rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1')

def image_summary(image_path):
    # 1. Detect labels with Rekognition via helper VisionClient
    client = VisionClient(rekognition=rekognition)
    labels_raw = client.detect_labels(Image={'S3Object': {'Bucket': 'my-bucket', 'Name': image_path}})
    labels = normalize_labels(labels_raw)

    # 2. Get description (using Google Vision as an example of later-step model)
    from google.cloud import vision
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    vis = vision.ImageAnnotatorClient(credentials=creds)
    with open(image_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    resp = vis.annotate_image({'image': image, 'features': [vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES)]})
    description = normalize_description(resp.image_properties.description)

    # 3. Assemble summary JSON
    summary = {
        'labels': labels,
        'description': description
    }
    return summary
