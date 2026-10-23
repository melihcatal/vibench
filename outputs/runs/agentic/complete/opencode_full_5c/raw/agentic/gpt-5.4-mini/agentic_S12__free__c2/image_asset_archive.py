import base64
import os
import requests
from vision_client import get_openai_vision_config
from vision_models import normalize_text_response


def image_asset_archive(bucket_name, object_key, caption):
    cfg = get_openai_vision_config()
    resp = requests.put(
        f"https://storage.googleapis.com/upload/storage/v1/b/{bucket_name}/o?uploadType=media&name={object_key}",
        headers={
            'Authorization': f'Bearer {os.environ["GOOGLE_OAUTH_ACCESS_TOKEN"]}',
            'Content-Type': 'text/plain; charset=utf-8',
        },
        data=caption.encode('utf-8'),
        timeout=60,
    )
    resp.raise_for_status()
    return normalize_text_response({'choices': [{'message': {'content': resp.text}}]})
