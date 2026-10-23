from google.cloud import storage

def export_record_to_archive(record, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(record["id"])
    blob.upload_from_string(str(record))
    return blob.public_url