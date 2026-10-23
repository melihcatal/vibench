from storage_client import get_storage_client


def upload_object(bucket_name, object_name, file_path):
    client = get_storage_client()
    with open(file_path, "rb") as file_obj:
        client.upload_file(bucket_name, object_name, file_obj)
