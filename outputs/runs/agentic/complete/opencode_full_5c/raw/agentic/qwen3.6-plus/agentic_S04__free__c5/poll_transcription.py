import time
from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    BATCH_ENDPOINT,
    FILES_ENDPOINT,
    get_headers,
    validate_api_key,
    parse_verbose_json_response,
)
from speech_models import (
    BatchJobStatus,
    BatchStatus,
    TranscriptionResult,
    normalize_transcription_response,
)


def get_batch_job_status(job_id: str) -> BatchJobStatus:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    url = f"{BATCH_ENDPOINT}/{job_id}"
    response = httpx.get(
        url,
        headers=get_headers(),
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


def download_output_file(output_file_id: str) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    url = f"{FILES_ENDPOINT}/{output_file_id}/content"
    response = httpx.get(
        url,
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        timeout=60.0,
        follow_redirects=True,
    )
    response.raise_for_status()

    lines = response.text.strip().split("\n")
    results = []
    for line in lines:
        if line.strip():
            import json

            results.append(json.loads(line))
    return results


def poll_transcription_job(
    job_id: str,
    max_wait_seconds: int = 3600,
    poll_interval_seconds: int = 30,
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    elapsed = 0
    while elapsed < max_wait_seconds:
        status = get_batch_job_status(job_id)

        if status.status == BatchStatus.COMPLETED:
            if status.output_file_id:
                return download_output_file(status.output_file_id)
            else:
                raise RuntimeError("Job completed but no output file ID available")

        if status.status in (
            BatchStatus.FAILED,
            BatchStatus.EXPIRED,
            BatchStatus.CANCELLED,
        ):
            raise RuntimeError(f"Batch job failed with status: {status.status}")

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise TimeoutError(
        f"Polling timed out after {max_wait_seconds} seconds for job {job_id}"
    )


def poll_and_return_transcript(
    job_id: str,
    max_wait_seconds: int = 3600,
    poll_interval_seconds: int = 30,
) -> TranscriptionResult:
    raw_results = poll_transcription_job(
        job_id=job_id,
        max_wait_seconds=max_wait_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )

    if not raw_results:
        raise ValueError("No transcription results returned")

    first_result = raw_results[0]
    response_body = first_result.get("response", {}).get("body", {})

    return normalize_transcription_response(response_body)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        job_id = sys.argv[1]
        result = poll_and_return_transcript(job_id)
        print(f"Language: {result.language}")
        print(f"Duration: {result.duration}s")
        print(f"Transcript: {result.text}")
    else:
        print("Usage: python poll_transcription.py <job_id>")
