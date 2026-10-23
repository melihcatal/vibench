import assemblyai as aai
from typing import Dict, List, Any, Optional

def normalize_transcript_response(transcript: aai.Transcript) -> Dict[str, Any]:
    """Normalize AssemblyAI transcript response."""
    words: List[Dict[str, Any]] = []
    if transcript.words:
        words = [
            {
                "text": word.text,
                "start": word.start,
                "end": word.end,
                "confidence": getattr(word, "confidence", None),
            }
            for word in transcript.words
        ]
    
    utterances: List[Dict[str, Any]] = []
    if transcript.utterances:
        utterances = [
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "confidence": getattr(utterance, "confidence", None),
            }
            for utterance in transcript.utterances
        ]
    
    return {
        "id": transcript.id,
        "status": str(transcript.status),
        "text": getattr(transcript, "text", ""),
        "words": words,
        "utterances": utterances,
        "confidence": getattr(transcript, "confidence", None),
    }
