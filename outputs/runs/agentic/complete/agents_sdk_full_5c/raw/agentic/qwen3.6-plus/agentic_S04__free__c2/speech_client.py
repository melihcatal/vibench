"""
speech_client.py - Local configuration and client helper utilities for Batch Speech-to-Text.

Provides an AssemblyAI-specific client wrapper for submitting transcription jobs,
polling status, uploading audio, and retrieving results from the AssemblyAI API.

AssemblyAI API Base URL: https://api.assemblyai.com/v2
"""

from __future__ import annotations

import os
import time
import logging
from typing import Optional, Dict, Any

import requests

from speech_models import (
    TranscriptionRequest,
    TranscriptionResponse,
    TranscriptionStatus,
)

logger = logging.getLogger(__name__)

# AssemblyAI-specific configuration
ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
ASSEMBLYAI_UPLOAD_ENDPOINT = f"{ASSEMBLYAI_API_BASE}/upload"
ASSEMBLYAI_TRANSCRIPTION_ENDPOINT = f"{ASSEMBLYAI_API_BASE}/transcript"


class AssemblyAIConfig:
    """Load and manage AssemblyAI API configuration."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "AssemblyAI API key not found. Set ASSEMBLYAI_API_KEY environment variable."
            )
        self.base_url = ASSEMBLYAI_API_BASE
        self.timeout = 10
        self.poll_interval = 5
        self.max_polls = 120

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }


class AssemblyAIClient:
    """
    Client wrapper for AssemblyAI batch transcription API.
    Handles audio upload, job submission, polling, and result retrieval.
    """

    def __init__(self, config: Optional[AssemblyAIConfig] = None):
        self.config = config or AssemblyAIConfig()
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)

    def upload_audio(self, audio_path: str) -> str:
        """
        Upload a local audio file to AssemblyAI and return the audio URL.
        Uses AssemblyAI upload endpoint: POST https://api.assemblyai.com/v2/upload
        """
        with open(audio_path, "rb") as f:
            response = self.session.post(
                ASSEMBLYAI_UPLOAD_ENDPOINT,
                data=f,
                headers={"authorization": self.config.api_key},
                timeout=self.config.timeout,
            )
        response.raise_for_status()
        result = response.json()
        audio_url = result.get("upload_url")
        if not audio_url:
            raise RuntimeError(f"AssemblyAI upload failed: {result}")
        logger.info("Uploaded audio to AssemblyAI: %s", audio_url)
        return audio_url

    def submit_transcription(self, request: TranscriptionRequest) -> str:
        """
        Submit a transcription job to AssemblyAI.
        Returns the transcription job ID.
        POST https://api.assemblyai.com/v2/transcript
        """
        payload = request.to_payload()
        response = self.session.post(
            ASSEMBLYAI_TRANSCRIPTION_ENDPOINT,
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        result = response.json()
        job_id = result.get("id")
        if not job_id:
            raise RuntimeError(f"AssemblyAI submission failed: {result}")
        logger.info("Submitted transcription job to AssemblyAI: %s", job_id)
        return job_id

    def get_transcription_status(self, transcription_id: str) -> Dict[str, Any]:
        """
        Get the status of a transcription job from AssemblyAI.
        GET https://api.assemblyai.com/v2/transcript/{id}
        """
        url = f"{ASSEMBLYAI_TRANSCRIPTION_ENDPOINT}/{transcription_id}"
        response = self.session.get(url, timeout=self.config.timeout)
        response.raise_for_status()
        return response.json()

    def poll_until_complete(
        self,
        transcription_id: str,
        poll_interval: Optional[int] = None,
        max_polls: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Poll AssemblyAI until transcription is complete or errored.
        """
        interval = poll_interval or self.config.poll_interval
        max_attempts = max_polls or self.config.max_polls

        for attempt in range(max_attempts):
            result = self.get_transcription_status(transcription_id)
            status = result.get("status")
            logger.info(
                "AssemblyAI job %s status: %s (attempt %d/%d)",
                transcription_id,
                status,
                attempt + 1,
                max_attempts,
            )
            if status == TranscriptionStatus.COMPLETED:
                return result
            if status == TranscriptionStatus.ERROR:
                raise RuntimeError(
                    f"AssemblyAI transcription error: {result.get('error')}"
                )
            time.sleep(interval)

        raise TimeoutError(
            f"AssemblyAI transcription {transcription_id} did not complete within {max_attempts} polls"
        )

    def retrieve_transcription(self, transcription_id: str) -> TranscriptionResponse:
        """
        Retrieve completed transcription result from AssemblyAI.
        """
        raw = self.poll_until_complete(transcription_id)
        return TranscriptionResponse.from_assemblyai_response(raw, transcription_id)

    def close(self):
        self.session.close()


def create_client(api_key: Optional[str] = None) -> AssemblyAIClient:
    """Factory function to create an AssemblyAI client with configuration."""
    config = AssemblyAIConfig(api_key=api_key)
    return AssemblyAIClient(config)
