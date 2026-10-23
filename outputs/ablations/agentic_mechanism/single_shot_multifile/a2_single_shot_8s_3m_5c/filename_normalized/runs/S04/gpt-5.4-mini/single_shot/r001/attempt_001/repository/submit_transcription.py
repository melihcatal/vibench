import os
from typing import Any, Dict, Optional

import requests

from speech_client import get_client_config, build_headers, build_url, ensure_file_path, raise_for_api_error
from speech_models import SubmitTranscriptionRequest, TranscriptionJob


def submit_transcription(audio_path: str, language: Optional[str] = None, model: Optional[str] = None, callback_url: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> TranscriptionJob:
    config = get_client_config()
    file_path = ensure_file_path(audio_path)
    request = SubmitTranscriptionRequest(audio_path=file_path, language=language, model=model, callback_url=callback_url, metadata=metadata)
    url = build_url(config, "/v1/audio/transcriptions")
    headers = build_headers(config, multipart=True)
    data = request.to_form_data()
    with open(file_path, "rb") as audio_file:
        files = {"file": (os.path.basename(file_path), audio_file)}
        response = requests.post(url, headers=headers, data=data, files=files, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    return TranscriptionJob.from_api(response.json())
