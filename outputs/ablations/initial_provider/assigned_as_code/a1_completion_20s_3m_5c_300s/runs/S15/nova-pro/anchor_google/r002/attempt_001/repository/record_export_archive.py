from google.cloud import storage


def export_records_to_archive(records, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    for record in records:
        blob = bucket.blob(record['id'])
        blob.upload_from_string(str(record))