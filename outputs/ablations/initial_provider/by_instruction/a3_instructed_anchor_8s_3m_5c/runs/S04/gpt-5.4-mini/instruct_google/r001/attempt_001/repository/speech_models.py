from dataclasses import dataclass


@dataclass
class TranscriptRequest:
    audio_uri: str
    output_uri: str | None = None
    diarization: bool = False
    enable_word_timestamps: bool = False
    model: str = "chirp_2"
    language_codes: list[str] | None = None


def normalize_segments(segments):
    normalized = []
    for segment in segments or []:
        normalized.append(
            {
                "text": getattr(segment, "text", None) if not isinstance(segment, dict) else segment.get("text"),
                "start_time": getattr(segment, "start_time", None) if not isinstance(segment, dict) else segment.get("start_time"),
                "end_time": getattr(segment, "end_time", None) if not isinstance(segment, dict) else segment.get("end_time"),
                "speaker": getattr(segment, "speaker", None) if not isinstance(segment, dict) else segment.get("speaker"),
            }
        )
    return normalized


def normalize_words(words):
    normalized = []
    for word in words or []:
        normalized.append(
            {
                "word": getattr(word, "word", None) if not isinstance(word, dict) else word.get("word"),
                "start_time": getattr(word, "start_time", None) if not isinstance(word, dict) else word.get("start_time"),
                "end_time": getattr(word, "end_time", None) if not isinstance(word, dict) else word.get("end_time"),
            }
        )
    return normalized
