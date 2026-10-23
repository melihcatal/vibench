from typing import List, Dict
import re


def check_metric_annotations(annotations: List[str]) -> Dict[str, List[str]]:
    unsafe_patterns = [
        r"<script.*?>.*?</script>",
        r"on\w+=\".*?\"",
        r"javascript:",
        r"data:\s*text/html",
        r"<!--.*?-->.*?<script",
        r"\b(alert|eval|prompt|confirm|document\.cookie|window\.location)\b",
    ]

    results = {}

    for annotation in annotations:
        unsafe_matches = []
        for pattern in unsafe_patterns:
            if re.search(pattern, annotation, re.IGNORECASE):
                unsafe_matches.append(pattern)

        if unsafe_matches:
            results[annotation] = unsafe_matches

    return results
