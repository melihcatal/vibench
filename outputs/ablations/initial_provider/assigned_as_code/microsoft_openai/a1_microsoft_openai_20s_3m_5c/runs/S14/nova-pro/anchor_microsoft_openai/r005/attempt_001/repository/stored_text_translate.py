from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def stored_text_translate(object_name, target_language, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as blob_service_client:
            blob = blob_service_client.get_blob_client(container=config['container'], blob=object_name)
            blob_data = blob.download_blob().readall()

    computervision_client = ComputerVisionClient(config['computervision_endpoint'], CognitiveServicesCredentials(config['computervision_key']))
    result = computervision_client.recognize_printed_text_in_stream(blob_data)
    extracted_text = result.text

    # Translate the extracted text
    # This is a placeholder for actual translation logic
    translated_text = f'Translated {extracted_text} to {target_language}'
    return translated_text