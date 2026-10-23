import assemblyai as aai
from typing import Dict, Any, List


def get_standard_config() -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig()


def get_diarized_config() -> aai.TranscriptionConfig:
    return aai.TranscriptionConfig(speaker_labels=True)


def serialize_transcript(transcript: aai.Transcript) -> Dict[str, Any]:
    words: List[Dict[str, Any]] = []
    if hasattr(transcript, "words") and transcript.words:
        words = [
            {
                "text": word.text,
                "start": word.start / 1000.0,
                "end": word.end / 1000.0,
                "confidence": getattr(word, "confidence", None),
                "speaker": getattr(word, "speaker", None),
            }
            for word in transcript.words
        ]
    utterances: List[Dict[str, Any]] = []
    if hasattr(transcript, "utterances") and transcript.utterances:
        utterances = [
            {
                "text": utterance.text,
                "speaker": utterance.speaker,
                "start": utterance.start / 1000.0,
                "end": utterance.end / 1000.0,
                "word_count": len(getattr(utterance, "words", [])),
            }
            for utterance in transcript.utterances
        ]
    return {
        "id": getattr(transcript, "id", None),
        "text": getattr(transcript, "text", ""),
        "words": words,
        "utterances": utterances,
    }
