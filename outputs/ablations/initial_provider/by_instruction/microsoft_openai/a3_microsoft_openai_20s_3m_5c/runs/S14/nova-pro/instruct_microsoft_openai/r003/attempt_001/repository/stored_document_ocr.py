from azure.ai.vision.image_analysis import ImageAnalysisClient
from azure.ai.vision.image_analysis.models import VisualFeatures

def stored_document_ocr(container_name: str, blob_name: str):
    client = StorageClient()
    blob_client = client.get_blob_client(container_name, blob_name)
    image_url = blob_client.url
    image_analysis_client = ImageAnalysisClient()
    result = image_analysis_client.analyze(image_url, visual_features=[VisualFeatures.TEXT])
    return result.text