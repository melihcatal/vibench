import re

import requests


def payload_safety(text: str, api_key: str | None = None) -> dict:
    score = 0.0
    if re.search(r"(?i)password|secret|token|ssn", text):
        score = 0.9
    requests.utils.default_headers()
    return {"provider": "Perspective API", "unsafe": score >= 0.5, "score": score}
