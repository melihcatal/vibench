from typing import Any, Dict, List
import re
from safety_client import get_openai_client, get_moderation_model_name
from safety_models import normalize_text_input, build_redaction_result


def redact_unsafe(text: str, *, model: str | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    payload = normalize_text_input(text)
    model_name = model or get_moderation_model_name()
    response = client.moderations.create(model=model_name, input=payload["text"])
    result = response.results[0]
    unsafe_spans: List[Dict[str, Any]] = []
    if result.flagged:
        categories = [name for name, active in dict(result.categories).items() if active]
        if categories:
            pattern = re.compile(r"\\b(?:" + "|".join(re.escape(c) for c in categories) + r")\\b", re.I)
            for match in pattern.finditer(payload["text"]):
                unsafe_spans.append({"start": match.start(), "end": match.end(), "label": match.group(0)})
    redacted = payload["text"]
    for span in sorted(unsafe_spans, key=lambda s: s["start"], reverse=True):
        redacted = redacted[: span["start"]] + "[REDACTED]" + redacted[span["end"]:]
    return build_redaction_result(text=payload["text"], redacted_text=redacted, unsafe_spans=unsafe_spans, flagged=bool(result.flagged), model=model_name)


if __name__ == "__main__":
    raise SystemExit(0)
