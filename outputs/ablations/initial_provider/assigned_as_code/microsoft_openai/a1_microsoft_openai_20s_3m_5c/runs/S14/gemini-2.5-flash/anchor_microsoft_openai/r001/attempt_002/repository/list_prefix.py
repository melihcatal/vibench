from storage_client import get_blob_service_client

def list_prefix(payload):
    container_name = payload['container_name']
    prefix = payload.get('prefix', '')
    
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container=container_name)
    
    blob_list = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_list.append({
            'name': blob.name,
            'size': blob.size,
            'creation_time': blob.creation_time.isoformat() if blob.creation_time else None,
            'last_modified': blob.last_modified.isoformat() if blob.last_modified else None,
            'etag': blob.etag
        })
            
    return {'blobs': blob_list, 'container_name': container_name, 'prefix': prefix}
