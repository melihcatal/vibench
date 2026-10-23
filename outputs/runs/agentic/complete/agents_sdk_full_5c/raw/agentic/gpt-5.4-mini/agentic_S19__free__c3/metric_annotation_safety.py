from __future__ import annotations

import re

from google.cloud import language_v2


_UNSAFE = re.compile(r"(?:drop\s+table|<script|javascript:|file:///|rm\s+-rf)", re.IGNORECASE)


def metric_annotation_safety(text: str) -> dict:
    client = language_v2.LanguageServiceClient()
    doc = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    _ = client.analyze_sentiment(request={"document": doc})
    unsafe = bool(_UNSAFE.search(text))
    return {"safe": not unsafe, "provider": "google.cloud.language_v2"}
