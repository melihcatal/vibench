import re

import boto3


def metric_annotation_safety(payload, config=None):
    text = payload.get("text", "")
    unsafe = bool(re.search(r"<script|javascript:|on\w+\s*=|\bDROP\b", text, re.I))
    comprehend = boto3.client("comprehend", region_name=(config or {}).get("region"))
    language = comprehend.detect_dominant_language(Text=text).get("Languages", [{}])[0].get("LanguageCode") if text else None
    return {"safe": not unsafe, "language": language}
