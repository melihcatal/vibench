"""
Poll a transcription job and return the transcript.
Provider: Deepgram (api.deepgram.com)
SDK: deepgram-sdk for async batch transcription job polling.
"""

import time
import logging
from typing import Optional, Dict, Any

from speech_client import create_deepgram_client
from speech_models import normalize_deepgram_response, TranscriptionResponse

logger = logging.getLogger(__name__)

DEEPGRAM_API_HOST = "api.deepgram.com"
POLL_INTERVAL_SECONDS = 5
MAX_POLL_ATTEMPTS = 120  # Up to 10 minutes


def poll_transcription_job(
    request_id: str,
    poll_interval: int = POLL_INTERVAL_SECONDS,
    max_attempts: int = MAX_POLL_ATTEMPTS,
) -> Dict[str, Any]:
    """
    Poll a Deepgram transcription job until completion and return results.
    
    Uses Deepgram's API at api.deepgram.com to check job status.
    The nova-2 batch processing may take time for longer audio files.
    
    Args:
        request_id: The Deepgram request ID from submission
        poll_interval: Seconds between polling attempts
        max_attempts: Maximum number of polling attempts
        
    Returns:
        Dict containing status and transcription results
    """
    client = create_deepgram_client()
    listen_client = client.listen
    
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        
        try:
            # Poll Deepgram for request status
            response = listen.get_request(request_id)
            response_data = response.to_dict()
            
            status = response_data.get("response", {}).get("status", "unknown")
            logger.info(f"Deepgram job {request_id} status: {status} (attempt {attempt})")
            
            if status == "completed":
                # Retrieve completed transcription from Deepgram
                result = response_data.get("response", {})
                return {
                    "status": "completed",
                    "request_id": request_id,
                    "provider": "deepgram",
                    "api_host": DEEPGRAM_API_HOST,
                    "raw_response": result,
                    "normalized": normalize_deepgram_response(result),
                }
            elif status in ("failed", "error"):
                error_msg = response_data.get("response", {}).get("error", "Unknown error")
                return {
                    "status": "failed",
                    "request_id": request_id,
                    "provider": "deepgram",
                    "error": error_msg,
                }
            else:
                # Still processing (queued, processing, etc.)
                time.sleep(poll_interval)
                
        except Exception as e:
            logger.warning(f"Error polling Deepgram job {request_id}: {e}")
            time.sleep(poll_interval)
    
    return {
        "status": "timeout",
        "request_id": request_id,
        "provider": "deepgram",
        "error": f"Polling timed out after {max_attempts} attempts",
    }


def get_transcript_text(
    request_id: str,
    poll_interval: int = POLL_INTERVAL_SECONDS,
    max_attempts: int = MAX_POLL_ATTEMPTS,
) -> Optional[str]:
    """
    Poll for a transcription job and return just the transcript text.
    
    Returns the full transcript text from Deepgram's nova-2 model.
    """
    result = poll_transcription_job(
        request_id=request_id,
        poll_interval=poll_interval,
        max_attempts=max_attempts,
    )
    
    if result["status"] == "completed" and "normalized" in result:
        normalized: TranscriptionResponse = result["normalized"]
        return normalized.transcript_text
    
    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        transcript = get_transcript_text(sys.argv[1])
        if transcript:
            print(transcript)
        else:
            print("Transcription not available")
    else:
        print("Usage: python poll_transcription.py <request_id>")
