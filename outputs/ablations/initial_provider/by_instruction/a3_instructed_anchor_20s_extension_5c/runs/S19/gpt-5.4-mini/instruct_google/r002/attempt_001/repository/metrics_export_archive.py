from google.cloud import storage


def metrics_export_archive(bucket_name, source_path, destination_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(source_path)
    return {"bucket": bucket_name, "object": destination_name}
