from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    job_name: str
    media_uri: str
    media_format: Optional[str] = None
    language_code: str = 'en-US'
    output_bucket: Optional[str] = None
    identify_speakers: bool = False
    max_speakers: Optional[int] = None
    show_speaker_labels: bool = False
    show_alternatives: bool = False
    vocabulary_name: Optional[str] = None
    terminology_name: Optional[str] = None


@dataclass
class WordItem:
    start_time: Optional[float]
    end_time: Optional[float]
    content: str
    speaker_label: Optional[str] = None
    confidence: Optional[str] = None


@dataclass
class SegmentItem:
    start_time: Optional[float]
    end_time: Optional[float]
    speaker_label: Optional[str]
    content: str
    items: List[WordItem] = field(default_factory=list)


@dataclass
class TranscriptResult:
    job_name: str
    status: str
    transcript_text: Optional[str] = None
    transcript_uri: Optional[str] = None
    language_code: Optional[str] = None
    items: List[WordItem] = field(default_factory=list)
    segments: List[SegmentItem] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


def build_transcribe_kwargs(request: TranscriptionRequest) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        'TranscriptionJobName': request.job_name,
        'Media': {'MediaFileUri': request.media_uri},
        'LanguageCode': request.language_code,
    }
    if request.media_format:
        kwargs['MediaFormat'] = request.media_format
    if request.output_bucket:
        kwargs['OutputBucketName'] = request.output_bucket
    if request.identify_speakers:
        kwargs['Settings'] = {'ShowSpeakerLabels': True}
        if request.max_speakers is not None:
            kwargs['Settings']['MaxSpeakerLabels'] = request.max_speakers
    if request.show_alternatives:
        kwargs.setdefault('Settings', {})['ShowAlternatives'] = True
    if request.vocabulary_name:
        kwargs['Settings'] = kwargs.get('Settings', {})
        kwargs['Settings']['VocabularyName'] = request.vocabulary_name
    if request.terminology_name:
        kwargs['Settings'] = kwargs.get('Settings', {})
        kwargs['Settings']['VocabularyFilterMethod'] = 'remove'
        kwargs['Settings']['VocabularyFilterName'] = request.terminology_name
    return kwargs


def parse_transcript_payload(payload: Dict[str, Any]) -> TranscriptResult:
    job = payload.get('TranscriptionJob', {})
    transcript_uri = job.get('Transcript', {}).get('TranscriptFileUri')
    status = job.get('TranscriptionJobStatus', 'UNKNOWN')
    result = TranscriptResult(
        job_name=job.get('TranscriptionJobName', ''),
        status=status,
        transcript_uri=transcript_uri,
        language_code=job.get('LanguageCode'),
        raw=payload,
    )
    if isinstance(job.get('Transcript'), dict):
        result.transcript_text = job['Transcript'].get('TranscriptFileUri')
    return result
