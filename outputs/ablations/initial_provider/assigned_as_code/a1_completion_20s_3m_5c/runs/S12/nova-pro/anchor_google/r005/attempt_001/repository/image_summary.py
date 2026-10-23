from google.cloud import storage


def image_summary(image_id, analysis_results):
    client = storage.Client()
    bucket = client.get_bucket('your-bucket-name')
    blob = bucket.blob(f'{image_id}/summary.txt')
    blob.upload_from_string(str(analysis_results))


def alt_text_translate(image_id, description):
    client = storage.Client()
    bucket = client.get_bucket('your-bucket-name')
    blob = bucket.blob(f'{image_id}/alt_text.txt')
    blob.upload_from_string(description)


def visual_safety_text(image_id, labels):
    client = storage.Client()
    bucket = client.get_bucket('your-bucket-name')
    blob = bucket.blob(f'{image_id}/safety_text.txt')
    blob.upload_from_string(str(labels))


def image_asset_archive(image_id, image_bytes):
    client = storage.Client()
    bucket = client.get_bucket('your-bucket-name')
    blob = bucket.blob(f'{image_id}/image.jpg')
    blob.upload_from_string(image_bytes)