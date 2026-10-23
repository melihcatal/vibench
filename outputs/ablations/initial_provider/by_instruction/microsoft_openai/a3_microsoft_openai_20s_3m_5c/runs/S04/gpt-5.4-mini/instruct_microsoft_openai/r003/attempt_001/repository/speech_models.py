def normalize_words(words):
    normalized = []
    for item in words or []:
        normalized.append(
            {
                "word": getattr(item, "word", item.get("word")),
                "start": getattr(item, "start", item.get("start")),
                "end": getattr(item, "end", item.get("end")),
            }
        )
    return normalized


def normalize_segments(segments):
    normalized = []
    for item in segments or []:
        normalized.append(
            {
                "start": getattr(item, "start", item.get("start")),
                "end": getattr(item, "end", item.get("end")),
                "text": getattr(item, "text", item.get("text")),
                "speaker": getattr(item, "speaker", item.get("speaker", None)),
                "words": normalize_words(getattr(item, "words", item.get("words", []))),
            }
        )
    return normalized


def transcript_text(result):
    if isinstance(result, dict):
        if result.get("text"):
            return result["text"]
        segments = result.get("segments", [])
    else:
        if getattr(result, "text", None):
            return result.text
        segments = getattr(result, "segments", [])
    return " ".join((getattr(s, "text", s.get("text", "")) for s in segments)).strip()


def as_dict(result):
    if isinstance(result, dict):
        return result
    payload = {}
    for key in ("id", "status", "text", "language", "duration", "segments", "words"):
        if hasattr(result, key):
            payload[key] = getattr(result, key)
    return payload
