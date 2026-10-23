import os
from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    FILES_ENDPOINT,
    BATCH_ENDPOINT,
    get_headers,
    validate_api_key,
    build_batch_payload,
)
from speech_models import (
    AudioTranscriptionRequest,
    BatchJobRequest,
    BatchJobStatus,
    BatchStatus,
)


def upload_audio_file(file_path: str) -> str:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f, "application/octet-stream"),
        }
        data = {"purpose": "batch"}
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        response = httpx.post(
            FILES_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
            timeout=120.0,
        )
        response.raise_for_status()
        return response.json()["id"]


def create_batch_transcription_job(
    input_file_id: str,
    endpoint: str = "/v1/audio/transcriptions",
    completion_window: str = "24h",
) -> BatchJobStatus:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    payload = build_batch_payload(
        input_file_id=input_file_id,
        endpoint=endpoint,
        completion_window=completion_window,
    )

    response = httpx.post(
        BATCH_ENDPOINT,
        headers=get_headers(),
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()

    return BatchJobStatus(
        job_id=data["id"],
        status=BatchStatus(data["status"]),
        input_file_id=data["input_file_id"],
        output_file_id=data.get("output_file_id"),
        error_file_id=data.get("error_file_id"),
        created_at=data.get("created_at", 0),
        completed_at=data.get("completed_at"),
        total_requests=data.get("request_counts", {}).get("total", 0),
        completed_requests=data.get("request_counts", {}).get("completed", 0),
        failed_requests=data.get("request_counts", {}).get("failed", 0),
    )


def submit_transcription(
    file_path: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "verbose_json",
    temperature: float = 0.0,
) -> BatchJobStatus:
    request = AudioTranscriptionRequest(
        file_path=file_path,
        model=model,
        language=language,
        response_format=response_format,
        temperature=temperature,
    )

    file_id = upload_audio_file(request.file_path)
    job = create_batch_transcription_job(
        input_file_id=file_id,
        endpoint="/v1/audio/transcriptions",
    )

    return job


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        result = submit_transcription(audio_path)
        print(f"Job ID: {result.job_id}")
        print(f"Status: {result.status}")
        print(f"Input File ID: {result.input_file_id}")
    else:
        print("Usage: python submit_transcription.py <audio_file_path>")
