import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from storage_models import StoredDocumentOCRRequest, StoredDocumentOCRResponse
from storage_client import StorageClient # To potentially generate a SAS URL for the blob
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def stored_document_ocr(request: StoredDocumentOCRRequest) -> StoredDocumentOCRResponse:
    # Azure AI Vision credentials
    subscription_key = os.getenv("AZURE_VISION_SUBSCRIPTION_KEY")
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_VISION_SUBSCRIPTION_KEY and AZURE_VISION_ENDPOINT environment variables must be set.")

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Generate a SAS URL for the blob to be accessible by Azure AI Vision
    storage_client_instance = StorageClient().get_blob_service_client()
    account_name = storage_client_instance.account_name
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

    if not account_key:
        raise ValueError("AZURE_STORAGE_ACCOUNT_KEY environment variable not set for SAS token generation.")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=request.container_name,
        blob_name=request.blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=10) # Short-lived SAS token
    )
    blob_url = f"https://{account_name}.blob.core.windows.net/{request.container_name}/{request.blob_name}?{sas_token}"

    # Call the Read API for OCR
    read_response = computervision_client.read(blob_url, raw=True)
    # Get the operation location (URL with an ID at the end)
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break

    text_content = []
    if read_result.status == 'succeeded':
        for text_recognition_result in read_result.analyze_result.read_results:
            for line in text_recognition_result.lines:
                text_content.append(line.text)
    
    return StoredDocumentOCRResponse(text_content="\n".join(text_content))
