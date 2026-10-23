from typing import Literal, Optional

import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TimestampedTranscript


def timestamped_transcript(job_id: str, granularity: Literal["word", "segment"] = "word") -> TimestampedTranscript:
    config = get_client_config()
    url = build_url(config, f"/v1/audio/transcriptions/{job_id}/result")
    headers = build_headers(config)
    params = {"timestamps": granularity}
    response = requests.get(url, headers=headers, params=params, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    return TimestampedTranscript.from_api(response.json())
