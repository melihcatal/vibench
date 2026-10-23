import os
import time
import json
import requests
from typing import Optional, Dict, Any, BinaryIO

from speech_models import (
    AssemblyAIConfig,
    OpenAIConfig,
    TranscriptionRequest,
    TranscriptionJob,
    TranscriptionResult,
    TranscriptionStatus,
)


def get_assemblyai_config() -> AssemblyAIConfig:
    return AssemblyAIConfig.from_env()


def get_openai_config() -> OpenAIConfig:
    return OpenAIConfig.from_env()


def upload_audio_file(file_path: str, config: Optional[AssemblyAIConfig] = None) -> str:
    if config is None:
        config = get_assemblyai_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    upload_url = config.upload_url
    headers = {"authorization": config.api_key}
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, headers=headers, data=f, timeout=300)
    response.raise_for_status()
    return response.json().get("upload_url", "")


def submit_transcription_job(
    request: TranscriptionRequest, config: Optional[AssemblyAIConfig] = None
) -> TranscriptionJob:
    if config is None:
        config = get_assemblyai_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    if not request.audio_url and request.audio_file_path:
        request.audio_url = upload_audio_file(request.audio_file_path, config)
    if not request.audio_url:
        raise ValueError("Either audio_url or audio_file_path must be provided")
    payload = request.to_assemblyai_payload()
    headers = config.get_headers()
    response = requests.post(
        f"{config.base_url}/transcript",
        headers=headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionJob(
        job_id=data.get("id", ""),
        status=TranscriptionStatus(data.get("status", "queued")),
        audio_url=data.get("audio_url", request.audio_url),
    )


def get_transcription_status(
    job_id: str, config: Optional[AssemblyAIConfig] = None
) -> TranscriptionJob:
    if config is None:
        config = get_assemblyai_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    headers = config.get_headers()
    response = requests.get(
        f"{config.base_url}/transcript/{job_id}",
        headers=headers,
        timeout=config.timeout,
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionJob(
        job_id=data.get("id", ""),
        status=TranscriptionStatus(data.get("status", "queued")),
        audio_url=data.get("audio_url", ""),
        created_at=data.get("created"),
        completed_at=data.get("completed"),
        error=data.get("error"),
    )


def get_transcription_result(
    job_id: str, config: Optional[AssemblyAIConfig] = None
) -> TranscriptionResult:
    if config is None:
        config = get_assemblyai_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    headers = config.get_headers()
    response = requests.get(
        f"{config.base_url}/transcript/{job_id}",
        headers=headers,
        timeout=config.timeout,
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionResult.from_assemblyai_response(data)


def poll_until_complete(
    job_id: str,
    config: Optional[AssemblyAIConfig] = None,
    interval: float = 5.0,
    max_wait: float = 600.0,
) -> TranscriptionResult:
    if config is None:
        config = get_assemblyai_config()
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(
                f"Transcription job {job_id} did not complete within {max_wait}s"
            )
        job = get_transcription_status(job_id, config)
        if job.status == TranscriptionStatus.COMPLETED:
            return get_transcription_result(job_id, config)
        if job.status == TranscriptionStatus.ERROR:
            raise RuntimeError(f"Transcription job {job_id} failed: {job.error}")
        time.sleep(interval)


def call_openai_api(
    endpoint: str,
    payload: Dict[str, Any],
    config: Optional[OpenAIConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    headers = config.get_headers()
    url = f"{config.base_url}/{endpoint.lstrip('/')}"
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=config.timeout,
    )
    response.raise_for_status()
    return response.json()
