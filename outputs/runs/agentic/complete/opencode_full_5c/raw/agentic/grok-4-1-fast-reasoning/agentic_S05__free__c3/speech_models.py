from dataclasses import dataclass
from typing import Dict, Any, Optional
from deepgram import LiveOptions


@dataclass
class RecognizeConfig:
    model: str = "nova-2"
    language: str = "en-US"
    punctuate: bool = True
    interim_results: bool = True
    smart_format: bool = True


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool
    confidence: Optional[float] = None


def deepgram_live_options(config: RecognizeConfig) -> LiveOptions:
    return LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=config.interim_results,
        smart_format=config.smart_format,
    )


def parse_deepgram_transcript(result: Dict[str, Any]) -> TranscriptChunk:
    alternatives = result.get("channel", {}).get("alternatives", [])
    if not alternatives:
        return TranscriptChunk(text="", is_final=False)
    alt = alternatives[0]
    text = alt.get("transcript", "")
    is_final = result.get("speech_final", False)
    confidence = alt.get("confidence")
    return TranscriptChunk(text=text, is_final=is_final, confidence=confidence)
