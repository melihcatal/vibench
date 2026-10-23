from typing import Any, Dict, List

from safety_client import TisaneSafetyClient


def redact_unsafe(text: str, spans: List[Dict[str, Any]]):
    return TisaneSafetyClient().redact_spans(text, spans)
