import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _get(data: Dict[str, Any], *keys: str) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


@dataclass
class TranscriptSegment:
    start_time: float
    end_time: float
    speaker_label: Optional[str]
    text: str


def parse_transcribe_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    job = payload.get("TranscriptionJob", payload)
    return {
        "status": job.get("TranscriptionJobStatus"),
        "job_name": job.get("TranscriptionJobName"),
        "transcript_uri": _get(job, "Transcript", "TranscriptFileUri"),
        "failure_reason": job.get("FailureReason"),
    }


def transcript_from_json(text: str) -> Dict[str, Any]:
    data = json.loads(text)
    return data.get("results", {})


def segments_from_transcript(results: Dict[str, Any]) -> List[TranscriptSegment]:
    items = results.get("items", [])
    segments: List[TranscriptSegment] = []
    current_text: List[str] = []
    start_time = None
    end_time = None
    speaker = None
    for item in items:
        item_type = item.get("type")
        if item_type == "pronunciation":
            if start_time is None:
                start_time = float(item.get("start_time", 0.0))
            end_time = float(item.get("end_time", item.get("start_time", 0.0)))
            current_text.append(item.get("alternatives", [{}])[0].get("content", ""))
            if not speaker:
                speaker = item.get("speaker_label")
        elif item_type == "punctuation" and current_text:
            current_text[-1] += item.get("alternatives", [{}])[0].get("content", "")
        if item.get("end_of_segment") and current_text:
            segments.append(TranscriptSegment(start_time or 0.0, end_time or 0.0, speaker, " ".join(current_text).strip()))
            current_text = []
            start_time = None
            end_time = None
            speaker = None
    if current_text:
        segments.append(TranscriptSegment(start_time or 0.0, end_time or 0.0, speaker, " ".join(current_text).strip()))
    return segments
