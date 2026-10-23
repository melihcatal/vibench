import os
import requests
from.storage_client import get_storage_client

def stored_document_ocr(container_name, blob_name):
    blob_service_client = get_storage_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_url = blob_client.url
    response = requests.get(download_url)
    if response.status_code == 200:
        ocr_api_url = 'https://api.ocr.space/parse/image'
        params = {
            'apikey': os.getenv('OCR_SPACE_API_KEY'),
            'language': 'eng'
        }
        files = {'image': ('image.jpg', response.content)}
        ocr_response = requests.post(ocr_api_url, params=params, files=files)
        ocr_data = ocr_response.json()
        return ocr_data
    else:
        return None