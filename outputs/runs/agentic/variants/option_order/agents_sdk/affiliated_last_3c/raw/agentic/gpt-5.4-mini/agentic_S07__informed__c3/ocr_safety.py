from __future__ import annotations

from typing import Dict

import boto3

from document_models import normalize_text


def check_unsafe_content(text: str) -> Dict[str, object]:
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(TextSegments=[{"Text": normalize_text(text)}])
    return response
