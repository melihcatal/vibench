from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.vision.image_analysis import ImageAnalysisClient
from azure.ai.vision.image_analysis.models import VisualFeatures



def run_ocr_on_stored_document(config, object_name):
    with DefaultAzureCredential() as credential:
        storage_client = BlobServiceClient(config['account_url'], credential=credential)
        blob = storage_client.get_blob_client(container=config['container'], blob=object_name)
        image_data = blob.download_blob().readall()

        vision_client = ImageAnalysisClient(endpoint=config['vision_endpoint'], credential=credential)
        result = vision_client.analyze(image_data=image_data, visual_features=[VisualFeatures.READ])

        if result.read_result:
            return {'text': result.read_result.text}
        else:
            return {'error': 'OCR failed'}