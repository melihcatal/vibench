import os
import re
from typing import Dict

import boto3


def metric_annotation_safety(text: str) -> Dict[str, object]:
    comprehend = boto3.client("comprehend", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    entities = comprehend.detect_syntax(Text=text, LanguageCode=os.getenv("OBSERVABILITY_LANGUAGE", "en"))
    unsafe = bool(re.search(r"\b(password|secret|token|apikey|api key|credential)\b", text, re.IGNORECASE))
    return {"safe": not unsafe, "language": os.getenv("OBSERVABILITY_LANGUAGE", "en"), "syntax_items": entities.get("SyntaxTokens", [])}
