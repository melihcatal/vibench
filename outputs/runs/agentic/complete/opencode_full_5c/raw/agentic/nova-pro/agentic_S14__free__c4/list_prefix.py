from storage_client import get_storage_client


def list_prefix(bucket_name, prefix=""):
    client = get_storage_client()
    return client.list_objects(bucket_name, prefix)
