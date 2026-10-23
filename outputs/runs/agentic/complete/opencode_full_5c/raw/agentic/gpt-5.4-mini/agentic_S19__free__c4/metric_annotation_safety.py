import re

from openai import OpenAI

from observability_client import load_config


def metric_annotation_safety(text):
    client = OpenAI(api_key=load_config().openai_api_key)
    unsafe_patterns = [
        r"\b(password|secret|token|api key)\b",
        r"<script",
        r"drop\s+table",
    ]
    risky = any(re.search(pattern, text, re.I) for pattern in unsafe_patterns)
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    flagged = bool(moderation.results and moderation.results[0].flagged)
    return {"unsafe": risky or flagged, "flagged": flagged, "provider": "openai"}
