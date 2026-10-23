import assemblyai as aai
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class STTConfig:
    language_code: str = "en"
    speaker_labels: bool = False
    num_speakers: Optional[int] = None


def config_to_aai(stt_config: STTConfig) -> aai.TranscriptionConfig:
    kwargs = {"language_code": stt_config.language_code}
    if stt_config.speaker_labels:
        kwargs["speaker_labels"] = True
        if stt_config.num_speakers is not None:
            kwargs["num_speakers"] = stt_config.num_speakers
    return aai.TranscriptionConfig(**kwargs)


def parse_transcript(transcript: aai.Transcript) -> Dict[str, Any]:
    words = [
        {
            "start": word.start,
            "end": word.end,
            "text": word.text,
            "confidence": word.confidence,
            "speaker": getattr(word, "speaker", None),
        }
        for word in getattr(transcript, "words", [])
    ]
    utterances = [
        {
            "speaker": utterance.speaker,
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end,
            "confidence": getattr(utterance, "confidence", None),
        }
        for utterance in getattr(transcript, "utterances", [])
    ]
    return {
        "id": transcript.id,
        "status": str(transcript.status),
        "text": getattr(transcript, "text", ""),
        "word_timestamps": words,
        "speaker_utterances": utterances,
    }
