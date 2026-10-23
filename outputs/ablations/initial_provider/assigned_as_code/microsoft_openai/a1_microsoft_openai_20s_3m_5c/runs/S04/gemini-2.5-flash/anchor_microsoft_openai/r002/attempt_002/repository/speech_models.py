from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class TranscriptionPayload:
    audio_uri: str
    language_code: str
    job_name: Optional[str] = "transcription"
    diarization_enabled: bool = False
    word_level_timestamps_enabled: bool = False


@dataclass
class TranscriptionJobResult:
    job_id: str
    status: str
    display_name: str
    locale: str
    created_date_time: str
    last_action_date_time: str
    duration_in_seconds: Optional[float] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    files_url: Optional[str] = None


@dataclass
class TranscriptionFileResult:
    path: str
    kind: str
    name: str
    properties: Dict[str, Any]
    created_date_time: str


@dataclass
class DiarizationSegment:
    speaker_id: int
    text: str
    offset: str
    duration: str


@dataclass
class WordTimestamp:
    word: str
    offset: str
    duration: str


@dataclass
class SegmentResult:
    text: str
    offset: str
    duration: str
    words: Optional[List[WordTimestamp]] = None
    speaker_id: Optional[int] = None


@dataclass
class FullTranscriptionResult:
    display_name: str
    duration_in_seconds: float
    combined_recognized_phrases: List[Dict[str, Any]]
    recognized_phrases: List[Dict[str, Any]]


def normalize_transcription_job_result(api_response: Dict[str, Any]) -> TranscriptionJobResult:
    return TranscriptionJobResult(
        job_id=api_response['self'].split('/')[-1],
        status=api_response['status'],
        display_name=api_response['displayName'],
        locale=api_response['locale'],
        created_date_time=api_response['createdDateTime'],
        last_action_date_time=api_response['lastActionDateTime'],
        duration_in_seconds=api_response.get('durationInSeconds'),
        properties=api_response.get('properties', {}),
        files_url=api_response['files']
    )

def normalize_transcription_file_result(api_response: Dict[str, Any]) -> TranscriptionFileResult:
    return TranscriptionFileResult(
        path=api_response['self'],
        kind=api_response['kind'],
        name=api_response['name'],
        properties=api_response['properties'],
        created_date_time=api_response['createdDateTime']
    )

def parse_full_transcription_result(api_response: Dict[str, Any]) -> FullTranscriptionResult:
    return FullTranscriptionResult(
        display_name=api_response['RecognitionStatus'],
        duration_in_seconds=float(api_response['Duration'] / 10000000), # Azure returns duration in 100-nanosecond intervals
        combined_recognized_phrases=api_response.get('CombinedRecognizedPhrases', []),
        recognized_phrases=api_response.get('RecognizedPhrases', [])
    )

def parse_diarized_transcript(api_response: Dict[str, Any]) -> List[DiarizationSegment]:
    segments = []
    for phrase in api_response.get('recognized_phrases', []):
        if 'SpeakerId' in phrase:
            segments.append(DiarizationSegment(
                speaker_id=phrase['SpeakerId'],
                text=phrase['DisplayText'],
                offset=phrase['Offset'],
                duration=phrase['Duration']
            ))
    return segments

def parse_timestamped_transcript(api_response: Dict[str, Any]) -> List[SegmentResult]:
    segments = []
    for phrase in api_response.get('recognized_phrases', []):
        words = []
        for word_info in phrase.get('Words', []):
            words.append(WordTimestamp(
                word=word_info['Word'],
                offset=word_info['Offset'],
                duration=word_info['Duration']
            ))
        segments.append(SegmentResult(
            text=phrase['DisplayText'],
            offset=phrase['Offset'],
            duration=phrase['Duration'],
            words=words,
            speaker_id=phrase.get('SpeakerId')
        ))
    return segments
