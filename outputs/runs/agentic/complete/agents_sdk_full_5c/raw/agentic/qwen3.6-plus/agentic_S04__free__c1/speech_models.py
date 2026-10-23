"""
Define local request, response, and normalization helpers for Batch Speech-to-Text.
Models are tailored for Deepgram API response structures.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class TranscriptionRequest:
    """Request payload for submitting batch transcription."""
    audio_url: str
    model: str = "nova-2"
    language: str = "en"
    diarize: bool = False
    punctuate: bool = True
    utterances: bool = False
    smart_format: bool = True
    extra_options: Dict[str, Any] = field(default_factory=dict)

    def to_deepgram_options(self) -> dict:
        """Convert to Deepgram API options format."""
        return {
            "model": self.model,
            "language": self.language,
            "diarize": self.diarize,
            "punctuate": self.punctuate,
            "utterances": self.utterances,
            "smart_format": self.smart_format,
            **self.extra_options,
        }


@dataclass
class WordResult:
    """Single word with timing information from Deepgram."""
    word: str
    start: float
    end: float
    confidence: float = 1.0
    speaker: Optional[int] = None
    punctuated_word: Optional[str] = None


@dataclass
class UtteranceResult:
    """Speaker utterance with diarization information."""
    speaker: int
    text: str
    start: float
    end: float
    confidence: float = 1.0
    words: List[WordResult] = field(default_factory=list)


@dataclass
class TranscriptionResponse:
    """Normalized response from batch transcription job."""
    request_id: str
    model_type: str
    transcript_text: str
    words: List[WordResult] = field(default_factory=list)
    utterances: List[UtteranceResult] = field(default_factory=list)
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None


def normalize_deepgram_response(raw_response: dict) -> TranscriptionResponse:
    """
    Normalize a Deepgram API response into TranscriptionResponse.
    
    Provider: Deepgram (api.deepgram.com)
    Handles nova-2 model response structure.
    """
    results = raw_response.get("results", {})
    channels = results.get("channels", [])
    
    if not channels:
        return TranscriptionResponse(
            request_id=raw_response.get("metadata", {}).get("request_id", ""),
            model_type=raw_response.get("metadata", {}).get("model_info", {}).get("model", "unknown"),
            transcript_text="",
        )

    channel = channels[0]
    alternatives = channel.get("alternatives", [])
    
    if not alternatives:
        return TranscriptionResponse(
            request_id=raw_response.get("metadata", {}).get("request_id", ""),
            model_type=raw_response.get("metadata", {}).get("model_info", {}).get("model", "unknown"),
            transcript_text="",
        )

    alternative = alternatives[0]
    transcript_text = alternative.get("transcript", "")
    
    # Parse words with timing
    words = []
    for w in alternative.get("words", []):
        words.append(WordResult(
            word=w.get("word", ""),
            start=w.get("start", 0.0),
            end=w.get("end", 0.0),
            confidence=w.get("confidence", 1.0),
            punctuated_word=w.get("punctuated_word"),
        ))

    # Parse utterances with diarization
    utterances = []
    for u in results.get("utterances", []):
        utt_words = []
        for w in u.get("words", []):
            utt_words.append(WordResult(
                word=w.get("word", ""),
                start=w.get("start", 0.0),
                end=w.get("end", 0.0),
                confidence=w.get("confidence", 1.0),
                speaker=u.get("speaker"),
            ))
        
        utterances.append(UtteranceResult(
            speaker=u.get("speaker", -1),
            text=u.get("transcript", ""),
            start=u.get("start", 0.0),
            end=u.get("end", 0.0),
            confidence=u.get("confidence", 1.0),
            words=utt_words,
        ))

    metadata = raw_response.get("metadata", {})
    return TranscriptionResponse(
        request_id=metadata.get("request_id", ""),
        model_type=metadata.get("model_info", {}).get("model", "nova-2"),
        transcript_text=transcript_text,
        words=words,
        utterances=utterances,
        duration=metadata.get("duration", 0.0),
        metadata=metadata,
    )


def format_diarized_transcript(response: TranscriptionResponse) -> str:
    """Format a diarized transcript with speaker labels."""
    if not response.utterances:
        return response.transcript_text
    
    lines = []
    for utt in response.utterances:
        lines.append(f"Speaker {utt.speaker}: {utt.text}")
    return "\n".join(lines)


def format_timestamped_transcript(response: TranscriptionResponse) -> str:
    """Format transcript with word-level timestamps."""
    if not response.words:
        return response.transcript_text
    
    lines = []
    for w in response.words:
        speaker_tag = f" [S{w.speaker}]" if w.speaker is not None else ""
        lines.append(f"[{w.start:.2f}-{w.end:.2f}]{speaker_tag} {w.punctuated_word or w.word}")
    return "\n".join(lines)
