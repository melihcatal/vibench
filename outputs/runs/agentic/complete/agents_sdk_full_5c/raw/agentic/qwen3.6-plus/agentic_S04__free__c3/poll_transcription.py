"""
Poll a transcription job and return the transcript using Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Endpoint: speech.googleapis.com
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

import time
from typing import Optional, Dict, Any

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech
from google.longrunning import operations_pb2

from speech_client import get_speech_client, get_project_path, parse_recognition_results
from speech_models import BatchTranscriptionResponse, normalize_google_results_to_segments


def poll_transcription_job(
    operation_name: str,
    project_id: Optional[str] = None,
    timeout: int = 600,
    poll_interval: int = 15,
) -> Dict[str, Any]:
    """
    Poll a batch transcription job until completion and return results.

    Args:
        operation_name: The full operation name from submit_transcription
        project_id: Google Cloud project ID
        timeout: Maximum seconds to wait for completion
        poll_interval: Seconds between poll attempts

    Returns:
        Dict with status and transcript data.
    """
    client = speech_v2.SpeechClient()

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return {
                "status": "TIMEOUT",
                "error": f"Operation did not complete within {timeout} seconds",
            }

        get_op_request = operations_pb2.GetOperationRequest(name=operation_name)
        operation = client.get_operation(request=get_op_request)

        if operation.done:
            if operation.error.code != 0:
                return {
                    "status": "ERROR",
                    "error_code": operation.error.code,
                    "error_message": operation.error.message,
                }

            result = cloud_speech.BatchRecognizeResponse()
            if operation.result.ByteSize() > 0:
                result.CopyFrom(operation.result)

            segments = normalize_google_results_to_segments(result.results)

            return {
                "status": "COMPLETED",
                "segments": segments,
                "total_segments": len(segments),
                "raw_result": result,
            }

        time.sleep(poll_interval)


def get_transcription_status(
    operation_name: str,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get the current status of a transcription job without waiting.

    Returns:
        Dict with status information.
    """
    client = speech_v2.SpeechClient()

    get_op_request = operations_pb2.GetOperationRequest(name=operation_name)
    operation = client.get_operation(request=get_op_request)

    if operation.done:
        if operation.error.code != 0:
            return {
                "status": "ERROR",
                "error_code": operation.error.code,
                "error_message": operation.error.message,
            }
        return {"status": "COMPLETED", "done": True}

    return {
        "status": "RUNNING",
        "done": False,
        "metadata": dict(operation.metadata) if operation.metadata else {},
    }


def poll_and_parse_transcript(
    operation_name: str,
    project_id: Optional[str] = None,
    timeout: int = 600,
    poll_interval: int = 15,
) -> BatchTranscriptionResponse:
    """
    Poll a transcription job and return a normalized BatchTranscriptionResponse.
    """
    result = poll_transcription_job(
        operation_name=operation_name,
        project_id=project_id,
        timeout=timeout,
        poll_interval=poll_interval,
    )

    if result["status"] != "COMPLETED":
        return BatchTranscriptionResponse(
            job_id=operation_name,
            status=result["status"],
        )

    response = BatchTranscriptionResponse(
        job_id=operation_name,
        status="COMPLETED",
        results=result.get("segments", []),
        total_segments=result.get("total_segments", 0),
        has_diarization=any(s.speaker_tag for s in result.get("segments", [])),
        has_word_timestamps=any(s.words for s in result.get("segments", [])),
    )

    return response


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <operation_name>")
        sys.exit(1)

    operation_name = sys.argv[1]
    result = poll_and_parse_transcript(operation_name)

    print(f"Job Status: {result.status}")
    print(f"Total Segments: {result.total_segments}")
    print(f"Has Diarization: {result.has_diarization}")
    print(f"Has Word Timestamps: {result.has_word_timestamps}")

    for i, seg in enumerate(result.results):
        print(f"\nSegment {i}: {seg.transcript}")
        print(f"  Confidence: {seg.confidence:.4f}")
