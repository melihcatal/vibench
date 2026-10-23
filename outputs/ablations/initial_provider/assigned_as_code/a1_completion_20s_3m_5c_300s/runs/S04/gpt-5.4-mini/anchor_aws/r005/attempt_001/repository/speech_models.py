def normalize_segments(segments):
    normalized = []
    for segment in segments or []:
        normalized.append(
            {
                "start_time": segment.get("StartTime"),
                "end_time": segment.get("EndTime"),
                "speaker_label": segment.get("SpeakerLabel"),
                "items": segment.get("Items", []),
                "transcript": segment.get("Transcript"),
            }
        )
    return normalized


def normalize_words(items):
    normalized = []
    for item in items or []:
        normalized.append(
            {
                "start_time": item.get("StartTime"),
                "end_time": item.get("EndTime"),
                "type": item.get("Type"),
                "alternatives": item.get("Alternatives", []),
                "speaker_label": item.get("SpeakerLabel"),
            }
        )
    return normalized


def extract_transcript_text(result):
    transcript = result.get("results", {}).get("transcripts", [])
    if transcript:
        return transcript[0].get("transcript")
    return result.get("Transcript") or ""


def extract_items(result):
    return result.get("results", {}).get("items", [])
