import os
import boto3
import re
from typing import List
from safety_models import SafetyResult, CategoryScore


def redact_unsafe(text: str) -> str:
    comprehend = boto3.client("comprehend", region_name="us-east-1")
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", text)
    redacted_parts = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        resp = comprehend.detect_toxicity(Text=sent, LanguageCode="en")
        tox_score = resp["Result"]["ToxicityScore"]
        scores = [CategoryScore("toxicity", tox_score)]
        blocked = tox_score > 0.5
        if blocked:
            redacted_parts.append("[REDACTED]")
        else:
            redacted_parts.append(sent)
    return ". ".join(redacted_parts) + "."
