from storage_client import AzureBlobStorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from azure.core.exceptions import ResourceNotFoundError

def object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    client = AzureBlobStorageClient()
    try:
        blob_client = client.get_blob_client(request.container_name, request.blob_name)
        properties = blob_client.get_blob_properties()
        return ObjectMetadataResponse(
            success=True,
            name=properties.name,
            size=properties.size,
            creation_time=str(properties.creation_time),
            last_modified=str(properties.last_modified),
            e_tag=properties.etag,
            content_settings={
                "content_type": properties.content_settings.content_type,
                "content_encoding": properties.content_settings.content_encoding,
                "content_language": properties.content_settings.content_language,
                "content_disposition": properties.content_settings.content_disposition,
                "cache_control": properties.content_settings.cache_control,
                "content_md5": properties.content_settings.content_md5
            },
            metadata=properties.metadata
        )
    except ResourceNotFoundError:
        return ObjectMetadataResponse(success=False, error=f"Blob '{request.blob_name}' not found in container '{request.container_name}'.")
    except Exception as e:
        return ObjectMetadataResponse(success=False, error=str(e))
