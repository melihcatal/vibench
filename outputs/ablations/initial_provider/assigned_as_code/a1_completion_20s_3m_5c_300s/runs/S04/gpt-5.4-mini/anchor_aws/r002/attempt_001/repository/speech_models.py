from dataclasses import dataclass


def normalize_text(value):
    return " ".join(str(value).split())


def normalize_segments(segments):
    result = []
    for segment in segments or []:
        result.append(
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker"),
                "text": normalize_text(segment.get("text", "")),
            }
        )
    return result


@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str
    job_name: str | None = None


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript_text: str | None = None
    segments: list | None = None
    raw: dict | None = None
