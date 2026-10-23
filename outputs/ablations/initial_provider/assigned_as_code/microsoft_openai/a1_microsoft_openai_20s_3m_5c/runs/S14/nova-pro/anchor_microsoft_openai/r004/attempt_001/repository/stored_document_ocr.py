from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


def ocr_stored_document(config, object_name):
    credential = DefaultAzureCredential()
    blob_client = BlobServiceClient(config['account_url'], credential=credential)
    blob = blob_client.get_blob_client(container=config['container'], blob=object_name)
    download_stream = blob.download_blob()
    computervision_client = ComputerVisionClient(config['computervision_endpoint'], CognitiveServicesCredentials(config['computervision_key']))
    ocr_result = computervision_client.recognize_printed_text_in_stream(download_stream.content_as_bytes())
    return ocr_result.text
