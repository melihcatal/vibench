import time
import assemblyai as aai
from speech_client import get_assemblyai_client, ASSEMBLYAI_TRANSCRIBE_MODEL
from speech_models import DiarizationResult, normalize_diarization_response


def get_diarized_transcript(
    audio_url: str, auto_chapters: bool = False
) -> DiarizationResult:
    aai.settings.api_key = get_assemblyai_client().api_key
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2,
        model=ASSEMBLYAI_TRANSCRIBE_MODEL,
        auto_chapters=auto_chapters,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config)
    if transcript.status == aai.TranscriptStatus.error:
        return DiarizationResult(job_id="", text="", segments=[], speakers=[])
    raw = {
        "id": transcript.id,
        "text": transcript.text,
        "utterances": [
            {
                "text": utterance.text,
                "speaker": f"Speaker {utterance.speaker}",
                "start": utterance.start / 1000.0,
                "end": utterance.end / 1000.0,
            }
            for utterance in transcript.utterances or []
        ],
    }
    return normalize_diarization_response(raw)


def submit_diarization_job(audio_url: str) -> str:
    aai.settings.api_key = get_assemblyai_client().api_key
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.submit(audio_url, config)
    return transcript.id


def poll_diarization_job(
    transcript_id: str, max_wait_seconds: int = 300, poll_interval: int = 5
) -> DiarizationResult:
    aai.settings.api_key = get_assemblyai_client().api_key
    transcriber = aai.Transcriber()
    elapsed = 0
    while elapsed < max_wait_seconds:
        transcript = transcriber.get_transcript(transcript_id)
        if transcript.status == aai.TranscriptStatus.completed:
            raw = {
                "id": transcript.id,
                "text": transcript.text,
                "utterances": [
                    {
                        "text": utterance.text,
                        "speaker": f"Speaker {utterance.speaker}",
                        "start": utterance.start / 1000.0,
                        "end": utterance.end / 1000.0,
                    }
                    for utterance in transcript.utterances or []
                ],
            }
            return normalize_diarization_response(raw)
        elif transcript.status == aai.TranscriptStatus.error:
            return DiarizationResult(
                job_id=transcript_id, text="", segments=[], speakers=[]
            )
        time.sleep(poll_interval)
        elapsed += poll_interval
    return DiarizationResult(job_id=transcript_id, text="", segments=[], speakers=[])
