from google.cloud import aiplatform

from speech_models import normalize_segments, normalize_transcript


def archive_summary(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id", payload.get("project_id", "")), location=config.get("location", "us-central1"))
    transcript = normalize_transcript(payload)
    segments = normalize_segments(payload)
    summary = {
        "summary": transcript[:280],
        "segment_count": len(segments),
    }
    return summary
