from google.cloud import storage

def archive_image_analysis(image_id, analysis_results):
    client = storage.Client()
    bucket = client.bucket('your-bucket-name')
    blob = bucket.blob(f'image_analysis/{image_id}.json')
    blob.upload_from_string(str(analysis_results))