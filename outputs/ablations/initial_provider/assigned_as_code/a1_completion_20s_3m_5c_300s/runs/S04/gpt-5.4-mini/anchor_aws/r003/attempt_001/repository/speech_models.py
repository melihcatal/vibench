def normalize_transcript_uri(result):
    if isinstance(result, dict):
        uri = result.get("TranscriptFileUri")
        if uri:
            return uri
        transcript = result.get("Transcript") or {}
        return transcript.get("TranscriptFileUri")
    return None


def normalize_transcript_text(result):
    if isinstance(result, dict):
        transcript = result.get("Transcript") or {}
        text = transcript.get("Transcript")
        if text is not None:
            return text
        results = transcript.get("Results") or result.get("Results") or []
        parts = []
        for item in results:
            alternatives = item.get("Alternatives") or []
            if alternatives:
                content = alternatives[0].get("Transcript")
                if content:
                    parts.append(content)
        return " ".join(parts)
    return ""


def normalize_segments(result):
    if not isinstance(result, dict):
        return []
    transcript = result.get("Transcript") or result
    items = []
    for entry in transcript.get("Results") or []:
        alternatives = entry.get("Alternatives") or []
        if alternatives:
            alt = alternatives[0]
            items.append({
                "transcript": alt.get("Transcript"),
                "items": alt.get("Items") or [],
                "start_time": alt.get("StartTime"),
                "end_time": alt.get("EndTime"),
                "confidence": alt.get("Confidence"),
            })
    return items
