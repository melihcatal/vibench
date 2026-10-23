from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class WordInfo:
    word: str
    offset: int # in ticks (100-nanosecond units)
    duration: int # in ticks

@dataclass
class TranscriptionSegment:
    id: str
    text: str
    start_time: Optional[str] = None # ISO 8601 duration format, or seconds
    end_time: Optional[str] = None   # ISO 8601 duration format, or seconds
    words: List[WordInfo] = field(default_factory=list)
    speaker_id: Optional[str] = None

@dataclass
class TranscriptionResult:
    job_id: str
    status: str # e.g., "Running", "Completed", "Failed"
    transcript: Optional[str] = None
    segments: List[TranscriptionSegment] = field(default_factory=list)
    raw_response: Optional[dict] = None # To store the raw provider response if needed

@dataclass
class TranscriptionRequest:
    audio_file_uri: str # URI to the audio file in cloud storage
    locale: str = "en-US"
    enable_diarization: bool = False
    enable_word_timestamps: bool = False

# Helper function to normalize Azure Speech SDK results into our TranscriptionResult model
def normalize_azure_speech_result(sdk_result, job_id: str) -> TranscriptionResult:
    segments = []
    full_transcript = []

    # The Azure Speech SDK `recognized` event gives us one segment at a time.
    # This normalization is simplified, assuming `sdk_result` is from a single recognition event.
    # For a full batch job, you'd iterate through all results.

    text = sdk_result.text if hasattr(sdk_result, 'text') else ""
    full_transcript.append(text)

    words_info = []
    if hasattr(sdk_result, 'words') and sdk_result.words:
        for word in sdk_result.words:
            words_info.append(WordInfo(word=word.word, offset=word.offset, duration=word.duration))
    
    speaker_id = None
    if hasattr(sdk_result, 'properties') and sdk_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_SpeakerId) is not None:
         speaker_id = sdk_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_SpeakerId)

    segments.append(TranscriptionSegment(
        id="segment_1", # Simplified ID
        text=text,
        words=words_info,
        speaker_id=speaker_id
    ))

    return TranscriptionResult(
        job_id=job_id,
        status="Completed", # Assuming this is called after successful recognition
        transcript=" ".join(full_transcript), # Simplified, usually aggregated from multiple segments
        segments=segments,
        # raw_response=sdk_result # For debugging, if sdk_result can be serialized
    )

