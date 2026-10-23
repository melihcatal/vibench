import requests
from speech_client import load_config, speech_base_url, auth_headers
from speech_models import flatten_segments


def timestamped_transcript(job_id, config=None):
    config = load_config(config)
    files_url = f"{speech_base_url(config['region'])}/transcriptions/{job_id}/files"
    files = requests.get(files_url, headers=auth_headers(config), timeout=30)
    files.raise_for_status()
    items = files.json().get('values', [])
    output = []
    for item in items:
        content_url = item.get('links', {}).get('contentUrl')
        if content_url:
            result = requests.get(content_url, timeout=30)
            result.raise_for_status()
            output.extend(flatten_segments(result.json()))
    return {'segments': output}
