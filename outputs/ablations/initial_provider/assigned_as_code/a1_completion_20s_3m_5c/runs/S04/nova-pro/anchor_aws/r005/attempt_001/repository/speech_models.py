from typing import Dict, Any


def normalize_transcription_response(response: Dict[str, Any]) -> Dict[str, Any]:
    job = response["TranscriptionJob"]
    transcript = job.get("Transcript", {})
    items = transcript.get("Items", [])
    normalized_items = [{"start_time": item["start_time"], "end_time": item["end_time"], "text": item["alternatives"][0]["transcript"]} for item in items]
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "transcript": normalized_items
    }