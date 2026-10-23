def normalize_transcript_segments(results):
    segments = []
    for item in results:
        if isinstance(item, dict):
            transcript = item.get("transcript", "")
            words = item.get("words", [])
        else:
            transcript = getattr(item, "transcript", "")
            words = getattr(item, "words", [])
        segments.append({"transcript": transcript, "words": words})
    return segments


def extract_transcript_text(result):
    if isinstance(result, dict):
        return result.get("transcript", "")
    return getattr(result, "transcript", "")
