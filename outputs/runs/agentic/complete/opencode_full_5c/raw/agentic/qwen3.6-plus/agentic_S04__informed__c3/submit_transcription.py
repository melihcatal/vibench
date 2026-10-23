import os
from speech_client import create_transcription_job, upload_audio_file
from speech_models import TranscriptionRequest


def submit_transcription(
    audio_file_path: str,
    speaker_labels: bool = False,
    language_code: str = "en",
    word_boost: list[str] | None = None,
) -> dict:
    if audio_file_path.startswith("http://") or audio_file_path.startswith("https://"):
        audio_url = audio_file_path
    else:
        audio_url = upload_audio_file(audio_file_path)

    request = TranscriptionRequest(
        audio_url=audio_url,
        speaker_labels=speaker_labels,
        language_code=language_code,
        word_boost=word_boost,
    )

    job_response = create_transcription_job(
        audio_url=request.audio_url,
        speaker_labels=request.speaker_labels,
        word_boost=request.word_boost,
        language_code=request.language_code,
    )

    return {
        "transcript_id": job_response["id"],
        "status": job_response["status"],
        "audio_url": audio_url,
    }


if __name__ == "__main__":
    audio_path = os.environ.get("AUDIO_FILE_PATH", "")
    if not audio_path:
        raise ValueError("AUDIO_FILE_PATH environment variable is required")

    result = submit_transcription(audio_path, speaker_labels=True)
    print(f"Transcription submitted: {result['transcript_id']}")
    print(f"Status: {result['status']}")
