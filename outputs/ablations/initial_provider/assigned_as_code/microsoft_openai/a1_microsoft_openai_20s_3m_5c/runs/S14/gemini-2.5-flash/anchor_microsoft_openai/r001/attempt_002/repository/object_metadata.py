from storage_client import get_blob_service_client

def object_metadata(payload):
    container_name = payload['container_name']
    object_name = payload['object_name']
    
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=object_name)
    
    properties = blob_client.get_blob_properties()
    
    # Extract relevant metadata
    metadata = {
        'name': properties.name,
        'size': properties.size,
        'content_settings': {
            'content_type': properties.content_settings.content_type,
            'content_encoding': properties.content_settings.content_encoding,
            'content_language': properties.content_settings.content_language,
            'content_disposition': properties.content_settings.content_disposition,
            'cache_control': properties.content_settings.cache_control
        },
        'creation_time': properties.creation_time.isoformat() if properties.creation_time else None,
        'last_modified': properties.last_modified.isoformat() if properties.last_modified else None,
        'etag': properties.etag,
        'metadata': properties.metadata  # Custom metadata
    }
    
    return metadata
