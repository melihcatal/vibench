import os
import requests
from speech_client import load_config, speech_base_url, auth_headers
from speech_models import normalize_job


def poll_transcription(job_id, config=None):
    config = load_config(config)
    url = f"{speech_base_url(config['region'])}/transcriptions/{job_id}"
    response = requests.get(url, headers=auth_headers(config), timeout=30)
    response.raise_for_status()
    job = normalize_job(response.json())
    if job.get('status') in {'Succeeded', 'Failed'}:
        files_url = f"{speech_base_url(config['region'])}/transcriptions/{job_id}/files"
        files = requests.get(files_url, headers=auth_headers(config), timeout=30)
        files.raise_for_status()
        return {'job': job, 'files': files.json()}
    return {'job': job}
