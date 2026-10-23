import json
import os
from vision_client import get_azure_blob_service_client
from vision_models import ImageAnalysisResult, ArchiveResult

def archive_results(
    analysis: ImageAnalysisResult,
    container_name: str = "image-analysis-archive"
) -> ArchiveResult:
    """
    Archives the source image and its analysis results to Azure Blob Storage.

    Args:
        analysis: The ImageAnalysisResult object.
        container_name: The name of the blob container to use.

    Returns:
        An ArchiveResult object with the public URLs to the archived files.
    """
    blob_service_client = get_azure_blob_service_client()
    
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
    except Exception:
        # Container likely already exists, which is fine.
        container_client = blob_service_client.get_container_client(container_name)

    base_name = os.path.splitext(os.path.basename(analysis.source_image_path))[0]
    image_blob_name = f"{base_name}.jpg"
    metadata_blob_name = f"{base_name}_analysis.json"

    # 1. Upload the original image file
    image_blob_client = container_client.get_blob_client(image_blob_name)
    with open(analysis.source_image_path, "rb") as data:
        image_blob_client.upload_blob(data, overwrite=True)

    # 2. Upload the analysis metadata as a JSON file
    metadata_blob_client = container_client.get_blob_client(metadata_blob_name)
    metadata_json = analysis.model_dump_json(indent=2)
    metadata_blob_client.upload_blob(metadata_json, overwrite=True)

    return ArchiveResult(
        image_url=image_blob_client.url,
        metadata_url=metadata_blob_client.url,
        container_name=container_name,
    )
