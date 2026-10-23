import base64

from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client(project=config.get('gcp_project'))
    bucket = client.bucket(config['bucket'])
    name = payload.get('name', 'image-analysis-artifact.json')
    blob = bucket.blob(name)
    blob.upload_from_string(payload.get('content', '').encode('utf-8'), content_type='application/json')
    if payload.get('image_bytes'):
        image_blob = bucket.blob(payload.get('image_name', 'image.bin'))
        image_blob.upload_from_string(base64.b64decode(base64.b64encode(payload['image_bytes'])))
    return {'bucket': config['bucket'], 'object': name}
