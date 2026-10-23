import base64
from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client(project=config.get('project'))
    bucket = client.bucket(config['bucket'])
    image_name = payload.get('image_name', 'image')
    caption = payload.get('caption', '')
    blob = bucket.blob(config.get('object_name', f'{image_name}.json'))
    blob.upload_from_string(caption, content_type='application/json')
    return {'uri': f'gs://{config["bucket"]}/{blob.name}', 'encoded': base64.b64encode(caption.encode()).decode()}
