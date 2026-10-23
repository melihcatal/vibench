def normalize_transcript_result(response):
    job = response.get("TranscriptionJob", response)
    transcript = job.get("Transcript", {})
    return {
        "job_id": job.get("TranscriptionJobName"),
        "status": job.get("TranscriptionJobStatus") or job.get("status"),
        "transcript_uri": transcript.get("TranscriptFileUri") or job.get("TranscriptFileUri"),
        "language_code": job.get("LanguageCode"),
        "speaker_labels": job.get("Settings", {}).get("ShowSpeakerLabels", False),
    }


def normalize_segments(items):
    segments = []
    current = None
    for item in items or []:
        if item.get("type") == "pronunciation":
            entry = {
                "start_time": item.get("start_time"),
                "end_time": item.get("end_time"),
                "content": item.get("alternatives", [{}])[0].get("content"),
                "speaker": item.get("speaker_label"),
            }
            segments.append(entry)
            current = entry
        elif item.get("type") == "punctuation" and current:
            current["content"] = f'{current["content"]}{item.get("alternatives", [{}])[0].get("content", "")}'
    return segments


def build_translation_request(text, target_language, source_language=None):
    return {
        "text": text,
        "target_language": target_language,
        "source_language": source_language,
    }
