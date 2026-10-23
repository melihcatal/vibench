import os
import time
from speech_client import (
    create_transcription_job,
    upload_audio_file,
    get_transcription_status,
)
from speech_models import TranscriptionResult, normalize_assemblyai_response


def get_timestamped_transcript(
    job_id: str = None,
    audio_file_path: str = None,
    audio_url: str = None,
    language_code: str = "en",
) -> TranscriptionResult:
    if job_id:
        while True:
            response = get_transcription_status(job_id)
            status = response.get("status", "")
            if status == "completed":
                return normalize_assemblyai_response(response)
            elif status == "error":
                raise RuntimeError(
                    f"Transcription job {job_id} failed: {response.get('error')}"
                )
            time.sleep(5)

    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError(
            "Either job_id, audio_file_path, or audio_url must be provided"
        )

    job_response = create_transcription_job(
        audio_url=audio_url,
        language_code=language_code,
        word_timestamps=True,
    )
    job_id = job_response["id"]

    while True:
        response = get_transcription_status(job_id)
        status = response.get("status", "")
        if status == "completed":
            return normalize_assemblyai_response(response)
        elif status == "error":
            raise RuntimeError(
                f"Timestamped transcription job {job_id} failed: {response.get('error')}"
            )
        time.sleep(5)


def format_word_timestamps(result: TranscriptionResult) -> list:
    timestamped_words = []
    for word in result.words:
        timestamped_words.append(
            {
                "word": word.word,
                "start_ms": word.start_ms,
                "end_ms": word.end_ms,
                "confidence": word.confidence,
            }
        )
    return timestamped_words


if __name__ == "__main__":
    job_id = os.environ.get("TRANSCRIPTION_JOB_ID")
    audio_path = os.environ.get("AUDIO_FILE_PATH")
    url = os.environ.get("AUDIO_URL")
    result = get_timestamped_transcript(
        job_id=job_id, audio_file_path=audio_path, audio_url=url
    )
    for entry in format_word_timestamps(result):
        print(f"[{entry['start_ms']}ms - {entry['end_ms']}ms] {entry['word']}")
