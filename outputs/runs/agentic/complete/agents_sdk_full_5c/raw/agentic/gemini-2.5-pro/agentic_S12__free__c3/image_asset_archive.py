import json
import uuid
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from vision_client import get_azure_storage_connection_string
from vision_models import VisualAnalysis

def archive_analysis_results(
    analysis_results: VisualAnalysis, 
    container_name: str = "image-analysis-archive"
) -> str:
    """
    Archives image analysis artifacts and derived captions in Azure Blob Storage.
    
    :param analysis_results: The VisualAnalysis object to archive.
    :param container_name: The name of the blob container.
    :return: The URL of the archived blob.
    """
    connection_string = get_azure_storage_connection_string()
    if not connection_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set.")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
    except Exception:
        # Container likely already exists
        container_client = blob_service_client.get_container_client(container_name)

    # Generate a unique blob name
    blob_name = f"{datetime.utcnow().strftime('%Y-%m-%d')}/{uuid.uuid4()}.json"
    
    blob_client = container_client.get_blob_client(blob_name)
    
    # Serialize the Pydantic model to a JSON string
    analysis_json = analysis_results.model_dump_json(indent=2)
    
    blob_client.upload_blob(analysis_json.encode("utf-8"), overwrite=True)
    
    return blob_client.url
