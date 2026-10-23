from typing import Optional

import requests

from speech_client import get_client_config, build_headers, build_url, ensure_file_path, raise_for_api_error
from speech_models import DiarizationRequest, DiarizedTranscript


def diarized_transcript(audio_path: str, speakers: int = 2, language: Optional[str] = None, model: Optional[str] = None) -> DiarizedTranscript:
    config = get_client_config()
    file_path = ensure_file_path(audio_path)
    request = DiarizationRequest(audio_path=file_path, speakers=speakers, language=language, model=model)
    url = build_url(config, "/v1/audio/transcriptions")
    headers = build_headers(config, multipart=True)
    data = request.to_form_data()
    with open(file_path, "rb") as audio_file:
        files = {"file": (file_path.rsplit("/", 1)[-1], audio_file)}
        response = requests.post(url, headers=headers, data=data, files=files, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    return DiarizedTranscript.from_api(response.json())
