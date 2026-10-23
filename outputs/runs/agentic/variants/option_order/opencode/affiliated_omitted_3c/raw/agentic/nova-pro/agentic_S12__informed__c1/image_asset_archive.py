import google.cloud.storage as gcs


def image_asset_archive(bucket_name, object_name, local_file_path):
    storage_client = gcs.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file_path)
