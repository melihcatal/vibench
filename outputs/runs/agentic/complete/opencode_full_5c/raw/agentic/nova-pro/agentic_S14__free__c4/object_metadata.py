from storage_client import get_storage_client


def object_metadata(bucket_name, object_name):
    client = get_storage_client()
    return client.head_object(bucket_name, object_name)
