from typing import Iterator

import requests

from model_client import auth_params, default_headers, google_stream_url, model_name


def stream_completion(prompt: str, model: str = "gemini-2.0-flash") -> Iterator[str]:
    response = requests.post(
        google_stream_url(model_name(model)),
        params=auth_params(),
        headers=default_headers(),
        json={"contents": [{"role": "user", "parts": [{"text": prompt}]}]},
        stream=True,
        timeout=60,
    )
    response.raise_for_status()
    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            chunk = line[6:]
            if chunk.strip() == "[DONE]":
                break
            yield chunk
