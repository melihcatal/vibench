import json
from typing import Dict, Any, List

def normalize_transcription_job_status(aws_status: str) -> str:
    status_map = {
        "QUEUED": "PENDING",
        "IN_PROGRESS": "IN_PROGRESS",
        "COMPLETED": "COMPLETED",
        "FAILED": "FAILED",
        "COMPLETED_WITH_ERROR": "FAILED",
    }
    return status_map.get(aws_status, "UNKNOWN")

def parse_transcription_result(transcript_uri: str) -> Dict[str, Any]:
    import requests
    response = requests.get(transcript_uri)
    response.raise_for_status()
    return response.json()

def extract_transcript_text(transcription_result: Dict[str, Any]) -> str:
    return transcription_result.get("results", {}).get("transcripts", [{}])[0].get("transcript", "")

def extract_diarization_segments(transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = []
    items = transcription_result.get("results", {}).get("items", [])
    
    current_speaker = None
    current_text = []
    start_time = None
    end_time = None

    for item in items:
        if item["type"] == "pronunciation":
            speaker_label = item.get("speaker_label")
            if speaker_label and speaker_label != current_speaker:
                if current_speaker is not None:
                    segments.append({
                        "speaker": current_speaker,
                        "text": " ".join(current_text),
                        "start_time": start_time,
                        "end_time": end_time
                    })
                current_speaker = speaker_label
                current_text = [item["alternatives"][0]["content"]]
                start_time = item["start_time"]
                end_time = item["end_time"]
            else:
                current_text.append(item["alternatives"][0]["content"])
                end_time = item["end_time"]
        elif item["type"] == "punctuation":
            if current_text:
                current_text[-1] += item["alternatives"][0]["content"]
                end_time = item["end_time"]
    
    if current_speaker is not None:
        segments.append({
            "speaker": current_speaker,
            "text": " ".join(current_text),
            "start_time": start_time,
            "end_time": end_time
        })
    return segments

def extract_timestamped_words(transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    words = []
    items = transcription_result.get("results", {}).get("items", [])
    for item in items:
        if item["type"] == "pronunciation":
            words.append({
                "word": item["alternatives"][0]["content"],
                "start_time": item["start_time"],
                "end_time": item["end_time"],
            })
    return words

def extract_segment_timestamps(transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = []
    if 'segments' in transcription_result.get('results', {}):
        for segment in transcription_result['results']['segments']:
            segments.append({
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "text": segment["transcript"],
            })
    return segments
