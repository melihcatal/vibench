
import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio_file_uri: str
    language_code: str
    sample_rate_hertz: Optional[int] = None
    encoding: Optional[str] = None # e.g., LINEAR16, FLAC, MULAW

@dataclasses.dataclass
class WordInfo:
    word: str
    start_time: str # e.g., "1.23s"
    end_time: str   # e.g., "2.45s"
    confidence: Optional[float] = None

@dataclasses.dataclass
class Alternative:
    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[WordInfo]] = None

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[Alternative]
    channel_tag: Optional[int] = None

@dataclasses.dataclass
class BatchRecognitionResponse:
    results: List[SpeechRecognitionResult]
    total_audio_duration: Optional[str] = None # e.g., "60.0s"

def normalize_batch_response(raw_response: dict) -> BatchRecognitionResponse:
    """
    Normalizes a raw API response into a BatchRecognitionResponse object.
    Assumes a hypothetical raw response structure.
    """
    normalized_results = []
    for result_data in raw_response.get("results", []):
        alternatives = []
        for alt_data in result_data.get("alternatives", []):
            words = None
            if "words" in alt_data:
                words = [
                    WordInfo(
                        word=w["word"],
                        start_time=w["startTime"],
                        end_time=w["endTime"],
                        confidence=w.get("confidence")
                    ) for w in alt_data["words"]
                ]
            alternatives.append(
                Alternative(
                    transcript=alt_data["transcript"],
                    confidence=alt_data.get("confidence"),
                    words=words
                )
            )
        normalized_results.append(
            SpeechRecognitionResult(
                alternatives=alternatives,
                channel_tag=result_data.get("channelTag")
            )
        )
    return BatchRecognitionResponse(
        results=normalized_results,
        total_audio_duration=raw_response.get("totalAudioDuration")
    )
