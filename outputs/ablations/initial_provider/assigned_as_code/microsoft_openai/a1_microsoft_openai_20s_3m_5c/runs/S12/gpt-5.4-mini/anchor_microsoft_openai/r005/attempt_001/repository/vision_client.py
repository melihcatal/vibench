import os


def load_vision_config(config=None):
    config = config or {}
    return {
        'endpoint': config.get('endpoint') or os.environ.get('AZURE_VISION_ENDPOINT'),
        'api_key': config.get('api_key') or os.environ.get('AZURE_VISION_API_KEY'),
        'max_labels': int(config.get('max_labels', 10)),
        'max_words': int(config.get('max_words', 20)),
        'language': config.get('language') or os.environ.get('AZURE_VISION_LANGUAGE', 'en'),
        'output_format': config.get('output_format') or 'text',
        'container_name': config.get('container_name') or os.environ.get('AZURE_STORAGE_CONTAINER'),
        'connection_string': config.get('connection_string') or os.environ.get('AZURE_STORAGE_CONNECTION_STRING'),
    }


def require_image_bytes(payload):
    if 'image_bytes' in payload and payload['image_bytes'] is not None:
        return payload['image_bytes']
    if 'image_path' in payload:
        with open(payload['image_path'], 'rb') as f:
            return f.read()
    raise ValueError('payload must include image_bytes or image_path')
