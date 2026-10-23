from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranscriptionRequest:
    """Represents a request for a batch speech-to-text transcription.

    Attributes:
        gcs_uri: The Google Cloud Storage URI of the audio file.
        language_code: The BCP-47 language tag for the audio (e.g., "en-US").
        enable_automatic_punctuation: Whether to enable automatic punctuation.
        enable_speaker_diarization: Whether to enable speaker diarization.
        min_speaker_count: Minimum number of speakers for diarization.
        max_speaker_count: Maximum number of speakers for diarization.
    """
    gcs_uri: str
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_speaker_diarization: bool = False
    min_speaker_count: Optional[int] = None
    max_speaker_count: Optional[int] = None

@dataclass
class WordInfo:
    """Represents information about a transcribed word, including timestamps and speaker tag.

    Attributes:
        word: The transcribed word.
        start_time: The start time of the word in seconds.
        end_time: The end time of the word in seconds.
        speaker_tag: The speaker tag assigned to the word (if diarization is enabled).
    """
    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None

@dataclass
class TranscriptionResult:
    """Represents the full result of a speech-to-text transcription.

    Attributes:
        full_transcript: The concatenated transcript of all recognized speech.
        word_timestamps: A list of WordInfo objects with detailed word-level timings.
        operation_name: The name of the long-running operation that produced this result.
    """
    full_transcript: str
    word_timestamps: List[WordInfo] = field(default_factory=list)
    operation_name: str = ""

if __name__ == '__main__':
    # Example usage
    req = TranscriptionRequest(gcs_uri="gs://my-bucket/audio.wav")
    print(f"Example request: {req}")

    word1 = WordInfo(word="hello", start_time=0.1, end_time=0.5)
    word2 = WordInfo(word="world", start_time=0.6, end_time=1.0, speaker_tag=1)
    result = TranscriptionResult(
        full_transcript="hello world", 
        word_timestamps=[word1, word2],
        operation_name="projects/123/operations/abc"
    )
    print(f"Example result: {result}")
