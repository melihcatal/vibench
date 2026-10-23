from google.cloud import storage

def export_document_to_storage(document, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(document['id'] + '.json')
    blob.upload_from_string(str(document), content_type='application/json')