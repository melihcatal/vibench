from dataclasses import dataclass


@dataclass
class TranscriptionRequest:
    file_path: str
    prompt: str = ""
    language: str = ""
    diarize: bool = False
    timestamp_granularity: str = "segment"


@dataclass
class TranscriptResponse:
    text: str
    segments: list


def normalize_response(result):
    text = getattr(result, "text", "") or ""
    segments = []
    for item in getattr(result, "segments", []) or []:
        segments.append(
            {
                "start": getattr(item, "start", None),
                "end": getattr(item, "end", None),
                "text": getattr(item, "text", "") or "",
                "speaker": getattr(item, "speaker", None),
                "words": [
                    {
                        "start": getattr(word, "start", None),
                        "end": getattr(word, "end", None),
                        "word": getattr(word, "word", "") or "",
                    }
                    for word in (getattr(item, "words", []) or [])
                ],
            }
        )
    return TranscriptResponse(text=text, segments=segments)
