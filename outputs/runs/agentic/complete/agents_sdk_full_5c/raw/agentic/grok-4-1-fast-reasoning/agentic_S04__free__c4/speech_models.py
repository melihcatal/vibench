from typing import List, Dict, Any

def extract_plain_transcript(transcript: Any) -> str:
    return transcript.text if hasattr(transcript, 'text') else ""

def extract_diarized_transcript(transcript: Any) -> List[Dict[str, str]]:
    if not hasattr(transcript, 'utterances'):
        return []
    return [
        {
            "speaker": utterance.speaker,
            "text": utterance.text
        }
        for utterance in transcript.utterances
    ]

def extract_word_timestamps(transcript: Any) -> List[Dict[str, Any]]:
    if not hasattr(transcript, 'words'):
        return []
    return [
        {
            "text": word.text,
            "start": word.start / 1000.0,
            "end": word.end / 1000.0,
            "confidence": getattr(word, 'confidence', None)
        }
        for word in transcript.words
    ]