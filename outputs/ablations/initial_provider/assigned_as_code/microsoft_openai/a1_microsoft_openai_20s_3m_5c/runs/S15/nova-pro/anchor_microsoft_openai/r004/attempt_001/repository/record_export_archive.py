from google.cloud import storage


def export_record_archive(bucket_name, record):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(f'record_{record['id']}.json')
    blob.upload_from_string(str(record))
    return blob.public_url