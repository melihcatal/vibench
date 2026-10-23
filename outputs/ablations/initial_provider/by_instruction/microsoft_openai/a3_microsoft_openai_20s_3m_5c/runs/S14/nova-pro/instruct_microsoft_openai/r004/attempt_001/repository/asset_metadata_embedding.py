import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from.storage_client import get_storage_client

def asset_metadata_embedding(container_name, blob_name):
    blob_service_client = get_storage_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_url = blob_client.url
    response = requests.get(download_url)
    if response.status_code == 200:
        subscription_key = os.getenv('COMPUTER_VISION_SUBSCRIPTION_KEY')
        endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        image_data = response.content
        image_stream = io.BytesIO(image_data)
        description = computervision_client.describe_image_in_stream(image_stream)
        return description.captions[0].text
    else:
        return None