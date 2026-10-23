from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict
from google.cloud import speech_v1p1beta1 as speech


@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float
    confidence: float
    speaker_tag: Optional[int] = None


@dataclass
class StreamingRecognitionResult:
    transcript: str
    is_final: bool
    confidence: float
    stability: float
    start_time: float
    end_time: float
    language_code: str
    words: List[WordInfo] = field(default_factory=list)
    alternatives: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StreamingRequest:
    audio_content: Optional[bytes] = None
    streaming_config: Optional[Dict[str, Any]] = None


@dataclass
class StreamingResponse:
    results: List[StreamingRecognitionResult] = field(default_factory=list)
    speech_event_type: Optional[str] = None


def normalize_google_response(
    response: speech.StreamingRecognizeResponse,
) -> StreamingResponse:
    normalized_results = []
    for result in response.results:
        if not result.alternatives:
            continue

        best_alt = result.alternatives[0]
        start_time = (
            result.result_start_time.total_seconds()
            if result.result_start_time
            else 0.0
        )
        end_time = (
            result.result_end_time.total_seconds() if result.result_end_time else 0.0
        )

        words = []
        for w in best_alt.words:
            words.append(
                WordInfo(
                    word=w.word,
                    start_time=w.start_time.total_seconds() if w.start_time else 0.0,
                    end_time=w.end_time.total_seconds() if w.end_time else 0.0,
                    confidence=w.confidence,
                    speaker_tag=getattr(w, "speaker_tag", None),
                )
            )

        alternatives = []
        for alt in result.alternatives[1:]:
            alternatives.append(
                {
                    "transcript": alt.transcript,
                    "confidence": alt.confidence,
                }
            )

        normalized_results.append(
            StreamingRecognitionResult(
                transcript=best_alt.transcript,
                is_final=result.is_final,
                confidence=best_alt.confidence,
                stability=result.stability,
                start_time=start_time,
                end_time=end_time,
                language_code="",
                words=words,
                alternatives=alternatives,
            )
        )

    speech_event = None
    if hasattr(response, "speech_event_type"):
        event_map = {
            speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_EVENT_TYPE_UNSPECIFIED: "unspecified",
            speech.StreamingRecognizeResponse.SpeechEventType.END_OF_SINGLE_UTTERANCE: "end_of_single_utterance",
        }
        speech_event = event_map.get(response.speech_event_type, "unspecified")

    return StreamingResponse(
        results=normalized_results,
        speech_event_type=speech_event,
    )


def create_streaming_request(
    audio_content: Optional[bytes] = None,
    language_code: str = "en-US",
    model: str = "latest_long",
    sample_rate: int = 16000,
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
) -> speech.StreamingRecognizeRequest:
    if audio_content is None:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            model=model,
            enable_automatic_punctuation=enable_automatic_punctuation,
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=interim_results,
        )
        return speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    else:
        return speech.StreamingRecognizeRequest(audio_content=audio_content)


def merge_transcripts(
    results: List[StreamingRecognitionResult], include_partial: bool = True
) -> str:
    parts = []
    for r in results:
        if r.is_final or include_partial:
            parts.append(r.transcript)
    return " ".join(parts)


def extract_final_transcripts(results: List[StreamingRecognitionResult]) -> List[str]:
    return [r.transcript for r in results if r.is_final]


def result_to_dict(result: StreamingRecognitionResult) -> Dict[str, Any]:
    return {
        "transcript": result.transcript,
        "is_final": result.is_final,
        "confidence": result.confidence,
        "stability": result.stability,
        "start_time": result.start_time,
        "end_time": result.end_time,
        "language_code": result.language_code,
        "words": [asdict(w) for w in result.words],
        "alternatives": result.alternatives,
    }
