from typing import List, Dict, Any, Optional
import json

class TranscriptionRequestPayload:
    """
    Represents the payload structure for submitting a batch transcription job
    to the Azure Speech-to-Text REST API v3.0.
    """
    def __init__(
        self,
        content_urls: List[str],
        locale: str = "en-US",
        display_name: str = "Batch Transcription Job",
        diarization_enabled: bool = False,
        word_level_timestamps_enabled: bool = False,
        speakers_min_count: Optional[int] = None,
        speakers_max_count: Optional[int] = None,
        profanity_filter_mode: Optional[str] = None, # e.g., "Masked", "Removed", "Tags"
        **kwargs # For any other advanced properties
    ):
        self.contentUrls = content_urls
        self.locale = locale
        self.displayName = display_name
        self.properties = {
            "wordLevelTimestampsEnabled": word_level_timestamps_enabled,
            "diarizationEnabled": diarization_enabled,
        }
        if speakers_min_count is not None or speakers_max_count is not None:
            self.properties["diarization"] = {"speakers": {}}
            if speakers_min_count is not None:
                self.properties["diarization"]["speakers"]["minCount"] = speakers_min_count
            if speakers_max_count is not None:
                self.properties["diarization"]["speakers"]["maxCount"] = speakers_max_count
        if profanity_filter_mode:
            self.properties["profanityFilterMode"] = profanity_filter_mode
        
        # Add any extra kwargs directly to properties
        self.properties.update(kwargs)

    def to_json(self) -> str:
        """
        Converts the payload to a JSON string.
        """
        return json.dumps(self.__dict__)


class TranscriptionResultWord:
    """
    Represents a word with its timestamp information from a transcription result.
    """
    def __init__(self, word: str, offset: int, duration: int):
        self.word = word
        self.offset_ms = offset
        self.duration_ms = duration

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranscriptionResultWord':
        return cls(data.get("word"), data.get("offset"), data.get("duration"))


class TranscriptionResultPhrase:
    """
    Represents a recognized phrase from a transcription result, including speaker info.
    """
    def __init__(
        self, 
        display_text: str,
        offset: int,
        duration: int,
        speaker_id: Optional[int] = None,
        words: Optional[List[TranscriptionResultWord]] = None
    ):
        self.display_text = display_text
        self.offset_ms = offset
        self.duration_ms = duration
        self.speaker_id = speaker_id
        self.words = words if words is not None else []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TranscriptionResultPhrase':
        n_best = data.get("nBest", [{}])[0]
        words = [TranscriptionResultWord.from_dict(w) for w in n_best.get("words", [])]
        return cls(
            display_text=n_best.get("display"),
            offset=data.get("offset"),
            duration=data.get("duration"),
            speaker_id=data.get("speaker"),
            words=words
        )

def parse_transcription_result(result_json: Dict[str, Any]) -> List[TranscriptionResultPhrase]:
    """
    Parses the full JSON output of an Azure Batch Speech-to-Text transcription
    result file into a list of TranscriptionResultPhrase objects.
    """
    phrases = []
    for phrase_data in result_json.get("recognizedPhrases", []):
        phrases.append(TranscriptionResultPhrase.from_dict(phrase_data))
    return phrases


# Example usage (for demonstration, not executed directly)
if __name__ == "__main__":
    # Example Transcription Request Payload
    request_payload = TranscriptionRequestPayload(
        content_urls=["https://example.blob.core.windows.net/audio/meeting.wav"],
        locale="en-US",
        diarization_enabled=True,
        speakers_max_count=2,
        word_level_timestamps_enabled=True
    )
    print("Generated Request Payload (JSON):")
    print(request_payload.to_json())

    # Example Transcription Result Parsing (simulated JSON)
    sample_result_json = {
        "recognizedPhrases": [
            {
                "channel": 0,
                "speaker": 1,
                "offset": 500000,
                "duration": 1000000,
                "nBest": [
                    {
                        "confidence": 0.95,
                        "lexical": "hello world",
                        "display": "Hello world.",
                        "words": [
                            {"word": "Hello", "offset": 500000, "duration": 200000},
                            {"word": "world", "offset": 750000, "duration": 300000}
                        ]
                    }
                ]
            }
        ]
    }

    parsed_phrases = parse_transcription_result(sample_result_json)
    print("\nParsed Transcription Result:")
    for phrase in parsed_phrases:
        print(f"  Phrase: '{phrase.display_text}', Speaker: {phrase.speaker_id}, Offset: {phrase.offset_ms}ms, Duration: {phrase.duration_ms}ms")
        for word in phrase.words:
            print(f"    Word: '{word.word}', Offset: {word.offset_ms}ms, Duration: {word.duration_ms}ms")
