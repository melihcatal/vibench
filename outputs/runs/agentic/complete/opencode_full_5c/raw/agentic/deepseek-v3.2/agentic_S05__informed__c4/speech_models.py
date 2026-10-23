from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import google.cloud.speech as speech


@dataclass
class AudioConfig:
    """Configuration for audio input."""

    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: Optional[str] = None
    use_enhanced: bool = False
    profanity_filter: bool = False
    enable_word_time_offsets: bool = False


@dataclass
class StreamingRecognitionConfig:
    """Configuration for streaming recognition."""

    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    single_utterance: bool = False
    model: Optional[str] = None
    use_enhanced: bool = False
    profanity_filter: bool = False
    enable_word_time_offsets: bool = False


@dataclass
class RecognitionResult:
    """Normalized recognition result."""

    transcript: str
    confidence: float
    is_final: bool
    language_code: str
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StreamingResponse:
    """Normalized streaming response."""

    results: List[RecognitionResult]
    speech_event_type: Optional[str] = None


def normalize_recognition_response(
    response: speech.RecognizeResponse,
) -> List[RecognitionResult]:
    """Normalize Google Cloud Speech recognition response."""
    results = []

    for result in response.results:
        alternatives = []

        for alt in result.alternatives:
            alternative_data = {
                "transcript": alt.transcript,
                "confidence": alt.confidence,
            }

            if hasattr(alt, "words"):
                alternative_data["words"] = [
                    {
                        "word": w.word,
                        "start_time": w.start_time.total_seconds()
                        if hasattr(w.start_time, "total_seconds")
                        else 0,
                        "end_time": w.end_time.total_seconds()
                        if hasattr(w.end_time, "total_seconds")
                        else 0,
                    }
                    for w in alt.words
                ]

            alternatives.append(alternative_data)

        main_alt = result.alternatives[0] if result.alternatives else None

        recognition_result = RecognitionResult(
            transcript=main_alt.transcript if main_alt else "",
            confidence=main_alt.confidence if main_alt else 0.0,
            is_final=True,
            language_code="",  # Would need to be passed separately
            alternatives=alternatives,
            words=alternatives[0].get("words", []) if alternatives else [],
        )

        results.append(recognition_result)

    return results


def normalize_streaming_response(streaming_response) -> StreamingResponse:
    """Normalize Google Cloud Speech streaming response."""
    results = []

    for result in streaming_response.results:
        alternatives = []

        for alt in result.alternatives:
            alternative_data = {
                "transcript": alt.transcript,
                "confidence": alt.confidence,
            }

            if hasattr(alt, "words"):
                alternative_data["words"] = [
                    {
                        "word": w.word,
                        "start_time": w.start_time.total_seconds()
                        if hasattr(w.start_time, "total_seconds")
                        else 0,
                        "end_time": w.end_time.total_seconds()
                        if hasattr(w.end_time, "total_seconds")
                        else 0,
                    }
                    for w in alt.words
                ]

            alternatives.append(alternative_data)

        main_alt = result.alternatives[0] if result.alternatives else None

        recognition_result = RecognitionResult(
            transcript=main_alt.transcript if main_alt else "",
            confidence=main_alt.confidence if main_alt else 0.0,
            is_final=result.is_final,
            language_code="",  # Would need to be passed separately
            alternatives=alternatives,
            words=alternatives[0].get("words", []) if alternatives else [],
        )

        results.append(recognition_result)

    speech_event_type = None
    if hasattr(streaming_response, "speech_event_type"):
        speech_event_type = (
            streaming_response.speech_event_type.name
            if streaming_response.speech_event_type
            else None
        )

    return StreamingResponse(results=results, speech_event_type=speech_event_type)


def create_speech_config(audio_config: AudioConfig) -> speech.RecognitionConfig:
    """Create Google Cloud Speech RecognitionConfig from AudioConfig."""
    from speech_client import get_audio_encoding

    config = speech.RecognitionConfig(
        encoding=get_audio_encoding(audio_config.encoding),
        sample_rate_hertz=audio_config.sample_rate_hertz,
        language_code=audio_config.language_code,
        enable_automatic_punctuation=audio_config.enable_automatic_punctuation,
        use_enhanced=audio_config.use_enhanced,
        profanity_filter=audio_config.profanity_filter,
    )

    if audio_config.model:
        config.model = audio_config.model

    if audio_config.enable_word_time_offsets:
        config.enable_word_time_offsets = True

    return config


def create_streaming_speech_config(
    streaming_config: StreamingRecognitionConfig,
) -> speech.StreamingRecognitionConfig:
    """Create Google Cloud Speech StreamingRecognitionConfig from StreamingRecognitionConfig."""
    from speech_client import get_audio_encoding

    config = speech.RecognitionConfig(
        encoding=get_audio_encoding(streaming_config.encoding),
        sample_rate_hertz=streaming_config.sample_rate_hertz,
        language_code=streaming_config.language_code,
        enable_automatic_punctuation=streaming_config.enable_automatic_punctuation,
        use_enhanced=streaming_config.use_enhanced,
        profanity_filter=streaming_config.profanity_filter,
    )

    if streaming_config.model:
        config.model = streaming_config.model

    if streaming_config.enable_word_time_offsets:
        config.enable_word_time_offsets = True

    streaming_recognition_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=streaming_config.interim_results,
        single_utterance=streaming_config.single_utterance,
    )

    return streaming_recognition_config
