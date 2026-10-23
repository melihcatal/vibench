from __future__ import annotations

import os
from typing import Dict

import boto3


def check_secret_label_safety(label: str, note: str) -> Dict[str, object]:
    comprehend = boto3.client("comprehend")
    sentiment = comprehend.detect_sentiment(Text=f"{label}\n{note}", LanguageCode="en")
    unsafe = sentiment.get("Sentiment") in {"NEGATIVE", "MIXED"}
    return {"service": "Amazon Comprehend", "label": label, "unsafe": unsafe, "sentiment": sentiment.get("Sentiment")}
