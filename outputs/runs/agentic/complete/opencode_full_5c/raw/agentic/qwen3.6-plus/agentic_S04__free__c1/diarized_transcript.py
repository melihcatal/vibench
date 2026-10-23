from typing import Optional

from speech_client import submit_transcription_job, upload_audio_file
from speech_models import DiarizationRequest, TranscriptionResult, Utterance


def request_diarized_transcription(
    audio_file_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: str = "en",
    speakers_expected: Optional[int] = None,
) -> TranscriptionResult:
    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError("Either audio_file_path or audio_url must be provided")

    request = DiarizationRequest(
        audio_url=audio_url,
        language_code=language_code,
        speakers_expected=speakers_expected,
    )

    response = submit_transcription_job(
        audio_url=request.audio_url,
        language_code=request.language_code,
        speaker_labels=True,
    )

    return TranscriptionResult.from_assemblyai_response(response)


def get_meeting_participants(result: TranscriptionResult) -> list[str]:
    speakers = set()
    for utterance in result.utterances:
        if utterance.speaker:
            speakers.add(utterance.speaker)
    return sorted(speakers)


def format_diarized_transcript(result: TranscriptionResult) -> str:
    lines = []
    for utterance in result.utterances:
        lines.append(f"[{utterance.speaker}] {utterance.text}")
    return "\n".join(lines)


def get_speaker_segments(result: TranscriptionResult, speaker: str) -> list[Utterance]:
    return [u for u in result.utterances if u.speaker == speaker]
