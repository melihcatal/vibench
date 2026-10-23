from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class STTConfig:
    language_code: str = "en-US"
    media_format: str = "mp3"
    output_bucket: str | None = None
    settings: Optional[Dict[str, Any]] = None

def make_start_request(job_name: str, media_uri: str, config: STTConfig) -> Dict[str, Any]:
    request: Dict[str, Any] = {
        "TranscriptionJobName": job_name,
        "LanguageCode": config.language_code,
        "Media": {"MediaFileUri": media_uri},
        "OutputBucketName": config.output_bucket,
        "MediaFormat": config.media_format,
    }
    if config.settings:
        request["Settings"] = config.settings
    return request

def parse_transcript_result(data: Dict[str, Any]) -> str:
    results = data.get("results")
    if not results or not results.get("transcripts"):
        raise ValueError("Invalid transcription result: no transcripts found")
    return results["transcripts"][0]["transcript"]

def parse_word_timestamps(data: Dict[str, Any]) -> List[Dict[str, str]]:
    timestamps: List[Dict[str, str]] = []
    results = data.get("results")
    if not results or "items" not in results:
        return timestamps
    for item in results["items"]:
        start_time = item.get("start_time")
        end_time = item.get("end_time")
        if start_time and end_time:
            alternatives = item.get("alternatives", [])
            if alternatives:
                word = alternatives[0].get("content", "")
                if word:
                    timestamps.append({
                        "word": word,
                        "start_time": start_time,
                        "end_time": end_time,
                    })
    return timestamps