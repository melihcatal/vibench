from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    source_uri: str
    language_code: str = "en-US"
    model: str = "chirp_2"
    diarization: bool = False
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = True


def normalize_segments(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = result.get("results") or result.get("segments") or []
    normalized = []
    for seg in segments:
        alternatives = seg.get("alternatives") or [{}]
        transcript = alternatives[0].get("transcript", "")
        normalized.append({
            "transcript": transcript,
            "speaker": seg.get("speakerTag") or seg.get("speaker_tag"),
            "start_time": seg.get("startTime") or seg.get("start_time"),
            "end_time": seg.get("endTime") or seg.get("end_time"),
            "words": alternatives[0].get("words", []),
        })
    return normalized


def transcript_text(result: Dict[str, Any]) -> str:
    segments = normalize_segments(result)
    parts = [s["transcript"] for s in segments if s.get("transcript")]
    return "\n".join(parts)


def build_google_speech_payload(request: TranscriptionRequest) -> Dict[str, Any]:
    config: Dict[str, Any] = {
        "languageCode": request.language_code,
        "model": request.model,
        "enableAutomaticPunctuation": request.enable_automatic_punctuation,
    }
    if request.diarization:
        config["diarizationConfig"] = {"enableSpeakerDiarization": True}
    if request.enable_word_time_offsets:
        config["enableWordTimeOffsets"] = True
    return {"config": config, "audio": {"uri": request.source_uri}}


def extract_operation_name(response: Dict[str, Any]) -> Optional[str]:
    return response.get("name") or response.get("operation") or response.get("operationName")
