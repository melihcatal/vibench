from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class WordInfo:
    word: str
    offset: int # in ticks
    duration: int # in ticks

@dataclass
class SegmentInfo:
    offset: int # in ticks
    duration: int # in ticks
    text: str
    words: Optional[List[WordInfo]] = None
    speakerId: Optional[str] = None

@dataclass
class TranscriptionResult:
    display_text: str
    segments: List[SegmentInfo] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

def normalize_transcript_result(raw_json: Dict[str, Any]) -> TranscriptionResult:
    """
    Normalizes the raw JSON response from Azure Speech-to-Text into a TranscriptionResult object.
    """
    display_text = ""
    segments: List[SegmentInfo] = []

    # The structure of the Azure Speech-to-Text batch transcription result can be complex.
    # This normalization attempts to extract common information.
    if "recognizedPhrases" in raw_json:
        for phrase in raw_json["recognizedPhrases"]:
            text = phrase.get("display", "")
            display_text += text + " "
            
            words = []
            if "words" in phrase:
                for word_data in phrase["words"]:
                    words.append(WordInfo(
                        word=word_data.get("word", ""),
                        offset=word_data.get("offset", 0),
                        duration=word_data.get("duration", 0)
                    ))

            segments.append(SegmentInfo(
                offset=phrase.get("offset", 0),
                duration=phrase.get("duration", 0),
                text=text,
                words=words,
                speakerId=phrase.get("speaker", None) # Azure's diarization uses 'speaker' field
            ))
    elif "CombinedRecognizedPhrases" in raw_json:
        # For simpler scenarios without detailed phrase breakdown directly
        for phrase in raw_json["CombinedRecognizedPhrases"]:
            text = phrase.get("Lexical", "") # Or "Display" depending on desired output
            display_text += text + " "
            segments.append(SegmentInfo(0, 0, text))

    return TranscriptionResult(
        display_text=display_text.strip(),
        segments=segments,
        raw_response=raw_json
    )
