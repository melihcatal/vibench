from speech_models import normalize_event


def handle_partial_results(event):
    normalized = normalize_event(event)
    if normalized.text and not normalized.is_final:
        return {
            "type": "partial",
            "text": normalized.text,
            "confidence": normalized.confidence,
        }
    if normalized.text and normalized.is_final:
        return {
            "type": "final",
            "text": normalized.text,
            "confidence": normalized.confidence,
        }
    return {"type": "empty", "text": "", "confidence": None}
