import os
import time
from speech_client import (
    create_transcription_job,
    upload_audio_file,
    get_transcription_status,
)
from speech_models import (
    TranscriptionResult,
    TranscriptionJob,
    TranscriptionStatus,
    normalize_assemblyai_response,
)


def request_diarized_transcript(
    audio_file_path: str = None,
    audio_url: str = None,
    language_code: str = "en",
    num_speakers: int = None,
) -> TranscriptionResult:
    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError("Either audio_file_path or audio_url must be provided")

    payload_kwargs = {
        "audio_url": audio_url,
        "language_code": language_code,
        "speaker_labels": True,
        "word_timestamps": True,
    }
    if num_speakers:
        payload_kwargs["speakers_expected"] = num_speakers

    job_response = create_transcription_job(**payload_kwargs)
    job_id = job_response["id"]

    while True:
        response = get_transcription_status(job_id)
        status = response.get("status", "")

        if status == "completed":
            return normalize_assemblyai_response(response)
        elif status == "error":
            raise RuntimeError(
                f"Diarized transcription job {job_id} failed: {response.get('error')}"
            )

        time.sleep(5)


if __name__ == "__main__":
    audio_path = os.environ.get("AUDIO_FILE_PATH")
    url = os.environ.get("AUDIO_URL")
    speakers = os.environ.get("NUM_SPEAKERS")
    result = request_diarized_transcript(
        audio_file_path=audio_path,
        audio_url=url,
        num_speakers=int(speakers) if speakers else None,
    )
    for utt in result.utterances:
        print(f"Speaker {utt.speaker}: {utt.text}")
