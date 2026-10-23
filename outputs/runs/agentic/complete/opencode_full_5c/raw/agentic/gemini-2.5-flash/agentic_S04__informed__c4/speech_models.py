from dataclasses import dataclass, field
from typing import Optional, List

# AssemblyAI specific models
import assemblyai as aai


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_diarization: bool = False
    word_timestamps: bool = False

    def to_assemblyai_config(self) -> aai.TranscriptionConfig:
        return aai.TranscriptionConfig(
            audio_url=self.audio_url,
            diarization=self.speaker_diarization,
            word_boost=self.word_timestamps,  # word_boost enables word-level timestamps in AssemblyAI
        )


@dataclass
class TranscriptionResponse:
    job_id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[dict]] = None
    utterances: Optional[List[dict]] = None

    @classmethod
    def from_assemblyai_transcript(
        cls, transcript: aai.Transcript
    ) -> "TranscriptionResponse":
        words = None
        if transcript.words:
            words = [
                {
                    "word": w.text,
                    "start": w.start,
                    "end": w.end,
                    "confidence": w.confidence,
                }
                for w in transcript.words
            ]

        utterances = None
        if transcript.utterances:
            utterances = [
                {"speaker": u.speaker, "text": u.text, "start": u.start, "end": u.end}
                for u in transcript.utterances
            ]

        return cls(
            job_id=transcript.id,
            status=transcript.status.value,
            text=transcript.text,
            words=words,
            utterances=utterances,
        )
