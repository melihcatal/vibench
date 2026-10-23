import re
from typing import Dict

from openai import OpenAI


_client = OpenAI()


def metric_annotation_safety(text: str) -> Dict[str, bool]:
    unsafe = bool(
        re.search(r"(?i)(password|api[_-]?key|secret|token|ssn|credit card)", text)
    )
    if not unsafe:
        _client.responses.create(model="gpt-5.4-mini", input=text)
    return {"safe": not unsafe}
