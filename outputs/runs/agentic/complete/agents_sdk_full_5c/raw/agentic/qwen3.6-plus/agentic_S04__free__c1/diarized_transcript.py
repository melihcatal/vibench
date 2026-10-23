"""
Request speaker diarization for a recorded meeting.
Provider: Deepgram (api.deepgram.com)
SDK: deepgram-sdk with nova-2 model and diarize_v2 for speaker identification.
"""

import logging
from typing import Optional, Dict, Any, List

from speech_client import create_deepgram_client, build_deepgram_options
from speech_models import (
    normalize_deepgram_response,
    format_diarized_transcript,
    TranscriptionResponse,
    UtteranceResult,
)

logger = logging.getLogger(__name__)

DEEPGRAM_API_HOST = "api.deepgram.com"
DIARIZATION_MODEL = "nova-2"
DIARIZE_VERSION = "v2"


def submit_diarized_transcription(
    audio_url: str,
    language: str = "en",
) -> Dict[str, Any]:
    """
    Submit audio for transcription with speaker diarization via Deepgram.
    
    Uses Deepgram's api.deepgram.com with nova-2 model and diarize_v2
    to identify and separate different speakers in a meeting recording.
    
    Args:
        audio_url: URL to the audio file
        language: Language code for transcription
        
    Returns:
        Dict containing request ID and diarization configuration
    """
    client = create_deepgram_client()
    prerecorded_client = client.listen.prerecorded.v("1")
    
    # Configure Deepgram options for diarization
    options = build_deepgram_options(
        model=DIARIZATION_MODEL,
        language=language,
        diarize=True,
        diarize_version=DIARIZE_VERSION,
        utterances=True,
        punctuate=True,
        smart_format=True,
    )
    
    payload = {"url": audio_url}
    response = prerecorded_client.transcribe_url(payload, options)
    
    request_id = response.results.metadata.request_id
    logger.info(
        f"Submitted diarization request to Deepgram {DEEPGRAM_API_HOST}: {request_id}"
    )
    
    return {
        "request_id": request_id,
        "provider": "deepgram",
        "api_host": DEEPGRAM_API_HOST,
        "model": DIARIZATION_MODEL,
        "diarize_version": DIARIZE_VERSION,
        "status": "submitted",
    }


def get_diarized_transcript(
    request_id: str,
) -> TranscriptionResponse:
    """
    Retrieve and normalize a completed diarized transcription from Deepgram.
    
    Returns a TranscriptionResponse with utterances containing speaker labels.
    Provider: Deepgram api.deepgram.com with nova-2 model.
    """
    client = create_deepgram_client()
    listen_client = client.listen
    
    # Poll Deepgram for completed request
    response = listen_client.get_request(request_id)
    response_data = response.to_dict()
    
    status = response_data.get("response", {}).get("status", "unknown")
    if status != "completed":
        raise ValueError(
            f"Transcription job {request_id} is not completed (status: {status})"
        )
    
    raw_response = response_data.get("response", {})
    normalized = normalize_deepgram_response(raw_response)
    
    if not normalized.utterances:
        logger.warning("No utterances returned - diarization may not have been enabled")
    
    return normalized


def format_meeting_transcript(
    request_id: str,
) -> str:
    """
    Get and format a meeting transcript with speaker labels.
    
    Uses Deepgram's diarization to produce a readable meeting transcript
    with speaker identification from api.deepgram.com.
    """
    response = get_diarized_transcript(request_id)
    return format_diarized_transcript(response)


def get_speaker_segments(
    request_id: str,
) -> List[Dict[str, Any]]:
    """
    Extract speaker segments from a diarized Deepgram transcription.
    
    Returns list of segments with speaker ID, text, and timing.
    """
    response = get_diarized_transcript(request_id)
    
    segments = []
    for utterance in response.utterances:
        segments.append({
            "speaker": utterance.speaker,
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end,
            "duration": utterance.end - utterance.start,
            "confidence": utterance.confidence,
        })
    
    return segments


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        request_id = sys.argv[1]
        transcript = format_meeting_transcript(request_id)
        print(transcript)
    else:
        print("Usage: python diarized_transcript.py <request_id>")
