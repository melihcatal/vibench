from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = False
    word_timestamps: bool = False
    punctuate: bool = True
    format_text: bool = True
    dual_channel: bool = False
    custom_spelling: Optional[list[dict[str, str]]] = None
    filter_profanity: bool = False

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_labels,
            "word_timestamps": self.word_timestamps,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "dual_channel": self.dual_channel,
            "filter_profanity": self.filter_profanity,
        }
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        return payload


@dataclass
class WordInfo:
    word: str
    start: int
    end: int
    confidence: float
    speaker: Optional[str] = None

    @classmethod
    def from_assemblyai_word(cls, word_data: dict) -> "WordInfo":
        return cls(
            word=word_data["text"],
            start=word_data["start"],
            end=word_data["end"],
            confidence=word_data.get("confidence", 0.0),
            speaker=word_data.get("speaker"),
        )


@dataclass
class Utterance:
    speaker: str
    text: str
    start: int
    end: int
    words: list[WordInfo] = field(default_factory=list)

    @classmethod
    def from_assemblyai_utterance(cls, utt_data: dict) -> "Utterance":
        return cls(
            speaker=utt_data.get("speaker", "unknown"),
            text=utt_data["text"],
            start=utt_data["start"],
            end=utt_data["end"],
            words=[WordInfo.from_assemblyai_word(w) for w in utt_data.get("words", [])],
        )


@dataclass
class TranscriptionResult:
    transcript_id: str
    status: str
    text: str = ""
    words: list[WordInfo] = field(default_factory=list)
    utterances: list[Utterance] = field(default_factory=list)
    audio_duration: float = 0.0
    confidence: float = 0.0
    language_code: str = "en"
    error: Optional[str] = None

    @classmethod
    def from_assemblyai_response(cls, response: dict) -> "TranscriptionResult":
        words = [WordInfo.from_assemblyai_word(w) for w in response.get("words", [])]
        utterances = [
            Utterance.from_assemblyai_utterance(u)
            for u in response.get("utterances", [])
        ]
        return cls(
            transcript_id=response["id"],
            status=response["status"],
            text=response.get("text", ""),
            words=words,
            utterances=utterances,
            audio_duration=response.get("audio_duration", 0.0) / 1000.0,
            confidence=response.get("confidence", 0.0),
            language_code=response.get("language_code", "en"),
            error=response.get("error"),
        )


@dataclass
class DiarizationRequest:
    audio_url: str
    language_code: str = "en"
    speakers_expected: Optional[int] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
            "speaker_labels": True,
        }
        if self.speakers_expected:
            payload["speakers_expected"] = self.speakers_expected
        return payload


@dataclass
class TimestampedSegment:
    text: str
    start_ms: int
    end_ms: int
    words: list[WordInfo] = field(default_factory=list)

    @classmethod
    def from_utterance(cls, utterance: Utterance) -> "TimestampedSegment":
        return cls(
            text=utterance.text,
            start_ms=utterance.start,
            end_ms=utterance.end,
            words=utterance.words,
        )


@dataclass
class TranslationRequest:
    transcript_id: str
    target_language: str = "es"
    prompt_template: Optional[str] = None

    def to_lemur_payload(self) -> dict[str, Any]:
        prompt = self.prompt_template or (
            f"Translate the following transcript to {self.target_language}. "
            "Preserve speaker labels and formatting."
        )
        return {
            "transcript_ids": [self.transcript_id],
            "prompt": prompt,
            "final_model": "assemblyai-mistral-7b",
            "max_output_size": 3000,
        }


@dataclass
class TranslationResult:
    transcript_id: str
    target_language: str
    translated_text: str
    lemur_response_id: str

    @classmethod
    def from_lemur_response(
        cls, transcript_id: str, target_language: str, response: dict
    ) -> "TranslationResult":
        return cls(
            transcript_id=transcript_id,
            target_language=target_language,
            translated_text=response.get("response", ""),
            lemur_response_id=response.get("response_id", ""),
        )


@dataclass
class ModerationRequest:
    transcript_id: str
    categories: Optional[list[str]] = None

    def to_lemur_payload(self) -> dict[str, Any]:
        categories = self.categories or [
            "violence",
            "hate_speech",
            "sexual_content",
            "profanity",
            "pii",
        ]
        prompt = (
            "Review the following transcript for content moderation. "
            f"Flag any instances of: {', '.join(categories)}. "
            "Return a JSON object with categories as keys and arrays of flagged text segments as values."
        )
        return {
            "transcript_ids": [self.transcript_id],
            "prompt": prompt,
            "final_model": "assemblyai-mistral-7b",
            "max_output_size": 2000,
        }


@dataclass
class ModerationResult:
    transcript_id: str
    flagged_content: dict[str, list[str]]
    is_safe: bool
    lemur_response_id: str

    @classmethod
    def from_lemur_response(
        cls, transcript_id: str, response: dict
    ) -> "ModerationResult":
        response_text = response.get("response", "{}")
        import json

        try:
            flagged = json.loads(response_text)
        except json.JSONDecodeError:
            flagged = {}

        is_safe = all(len(v) == 0 for v in flagged.values()) if flagged else True
        return cls(
            transcript_id=transcript_id,
            flagged_content=flagged,
            is_safe=is_safe,
            lemur_response_id=response.get("response_id", ""),
        )


@dataclass
class SummaryRequest:
    transcript_id: str
    summary_type: str = "bullets"
    custom_prompt: Optional[str] = None

    def to_lemur_payload(self) -> dict[str, Any]:
        if self.custom_prompt:
            prompt = self.custom_prompt
        elif self.summary_type == "bullets":
            prompt = (
                "Summarize the following transcript as a bulleted list. "
                "Include key decisions, action items, and important topics discussed."
            )
        elif self.summary_type == "paragraph":
            prompt = (
                "Provide a concise paragraph summary of the following transcript. "
                "Focus on the main topics and outcomes."
            )
        else:
            prompt = "Summarize the following transcript."

        return {
            "transcript_ids": [self.transcript_id],
            "prompt": prompt,
            "final_model": "assemblyai-mistral-7b",
            "max_output_size": 1500,
        }


@dataclass
class SummaryResult:
    transcript_id: str
    summary_text: str
    summary_type: str
    lemur_response_id: str

    @classmethod
    def from_lemur_response(
        cls, transcript_id: str, summary_type: str, response: dict
    ) -> "SummaryResult":
        return cls(
            transcript_id=transcript_id,
            summary_text=response.get("response", ""),
            summary_type=summary_type,
            lemur_response_id=response.get("response_id", ""),
        )


@dataclass
class EmbeddingRequest:
    transcript_id: str
    chunk_size: int = 512
    overlap: int = 50

    def to_segments(self, result: TranscriptionResult) -> list[dict[str, Any]]:
        segments = []
        if result.utterances:
            for utt in result.utterances:
                segments.append(
                    {
                        "speaker": utt.speaker,
                        "text": utt.text,
                        "start_ms": utt.start,
                        "end_ms": utt.end,
                    }
                )
        elif result.words:
            current_text = []
            current_start = result.words[0].start
            for word in result.words:
                current_text.append(word.word)
                if len(current_text) >= self.chunk_size:
                    segments.append(
                        {
                            "speaker": word.speaker or "unknown",
                            "text": " ".join(current_text),
                            "start_ms": current_start,
                            "end_ms": word.end,
                        }
                    )
                    current_text = []
                    current_start = word.end
            if current_text:
                segments.append(
                    {
                        "speaker": result.words[-1].speaker or "unknown",
                        "text": " ".join(current_text),
                        "start_ms": current_start,
                        "end_ms": result.words[-1].end,
                    }
                )
        return segments


@dataclass
class SegmentEmbedding:
    text: str
    speaker: str
    start_ms: int
    end_ms: int
    embedding: list[float]
    segment_index: int

    @classmethod
    def from_segment(
        cls, segment: dict, embedding: list[float], index: int
    ) -> "SegmentEmbedding":
        return cls(
            text=segment["text"],
            speaker=segment.get("speaker", "unknown"),
            start_ms=segment["start_ms"],
            end_ms=segment["end_ms"],
            embedding=embedding,
            segment_index=index,
        )
