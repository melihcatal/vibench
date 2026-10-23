from speech_client import (
    create_transcription_job,
    upload_audio_file,
    get_transcription_result,
)
from speech_models import normalize_transcription_response, extract_diarized_utterances


def request_diarized_transcription(audio_url: str, **kwargs) -> dict:
    job = create_transcription_job(
        audio_url=audio_url,
        speaker_labels=True,
        **kwargs,
    )
    return job


def get_diarized_transcript(
    transcript_id: str,
    max_wait_seconds: int = 300,
    poll_interval_seconds: int = 5,
) -> list[dict]:
    import time

    elapsed = 0
    while elapsed < max_wait_seconds:
        response = get_transcription_result(transcript_id)
        status = response.get("status", "")

        if status == "completed":
            result = normalize_transcription_response(response)
            return extract_diarized_utterances(result)
        elif status == "error":
            raise RuntimeError(
                f"Diarization failed: {response.get('error', 'Unknown error')}"
            )

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise TimeoutError(
        f"Diarized transcription did not complete within {max_wait_seconds} seconds"
    )


def diarize_meeting_recording(
    audio_file_path: str,
    **kwargs,
) -> list[dict]:
    if audio_file_path.startswith("http://") or audio_file_path.startswith("https://"):
        audio_url = audio_file_path
    else:
        audio_url = upload_audio_file(audio_file_path)

    job = request_diarized_transcription(audio_url, **kwargs)
    transcript_id = job["id"]

    return get_diarized_transcript(transcript_id)


if __name__ == "__main__":
    import os

    audio_path = os.environ.get("AUDIO_FILE_PATH", "")
    if not audio_path:
        raise ValueError("AUDIO_FILE_PATH environment variable is required")

    utterances = diarize_meeting_recording(audio_path)
    for u in utterances:
        print(f"[{u['speaker']}]: {u['text']}")
