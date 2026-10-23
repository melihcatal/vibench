from dataclasses import dataclass


@dataclass
class TranscriptionRequest:
    audio_uri: str
    job_name: str
    language_code: str
    media_format: str = "mp3"
    diarization: bool = False
    show_speaker_labels: bool = False
    max_speaker_labels: int | None = None
    timestamps: bool = False


def normalize_transcript(result: dict) -> dict:
    transcript = result.get("results", {}).get("transcripts", [])
    items = result.get("results", {}).get("items", [])
    return {"transcripts": transcript, "items": items, "raw": result}
