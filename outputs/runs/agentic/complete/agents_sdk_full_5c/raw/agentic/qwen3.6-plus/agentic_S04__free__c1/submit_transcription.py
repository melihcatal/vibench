"""
Submit an audio file for batch transcription.
Provider: Deepgram (api.deepgram.com)
SDK: deepgram-sdk with nova-2 model for batch/prerecorded transcription.
"""

import os
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from speech_client import create_deepgram_client, build_deepgram_options
from speech_models import TranscriptionRequest

logger = logging.getLogger(__name__)

DEEPGRAM_API_HOST = "api.deepgram.com"
DEFAULT_MODEL = "nova-2"


def submit_audio_for_transcription(
    audio_source: str,
    model: str = DEFAULT_MODEL,
    language: str = "en",
    options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Submit an audio file (URL or local path) for batch transcription via Deepgram.
    
    Uses Deepgram's prerecorded/batch transcription API at api.deepgram.com.
    The nova-2 model provides high-accuracy speech recognition.
    
    Args:
        audio_source: URL to audio file or local file path
        model: Deepgram model identifier (e.g., 'nova-2', 'enhanced')
        language: Language code (e.g., 'en', 'es', 'fr')
        options: Additional Deepgram-specific options
        
    Returns:
        Dict containing the transcription request ID and status
    """
    client = create_deepgram_client()
    prerecorded_client = client.listen.prerecorded.v("1")
    
    # Build Deepgram-specific options for nova-2 model
    dg_options = build_deepgram_options(
        model=model,
        language=language,
        punctuate=True,
        smart_format=True,
        **(options or {}),
    )
    
    parsed = urlparse(audio_source)
    
    if parsed.scheme in ("http", "https"):
        # Submit URL directly to Deepgram
        payload = {"url": audio_source}
        response = prerecorded.transcribe_url(payload, dg_options)
        logger.info(f"Submitted URL {audio_source} to Deepgram {DEEPGRAM_API_HOST}")
    else:
        # Read local file and submit to Deepgram
        if not os.path.exists(audio_source):
            raise FileNotFoundError(f"Audio file not found: {audio_source}")
        
        with open(audio_source, "rb") as audio_file:
            buffer = audio_file.read()
        
        response = prerecorded.transcribe_file(
            {"buffer": buffer},
            dg_options,
        )
        logger.info(f"Submitted local file {audio_source} to Deepgram {DEEPGRAM_API_HOST}")
    
    # Extract request metadata from Deepgram response
    request_id = response.results.metadata.request_id
    model_info = response.results.metadata.model_info
    
    return {
        "request_id": request_id,
        "status": "submitted",
        "model": model_info.model if model_info else model,
        "provider": "deepgram",
        "api_host": DEEPGRAM_API_HOST,
        "audio_source": audio_source,
    }


def submit_meeting_audio(
    meeting_audio_path: str,
    enable_diarization: bool = True,
    enable_utterances: bool = True,
) -> Dict[str, Any]:
    """
    Submit a recorded meeting for batch transcription with meeting-optimized settings.
    
    Uses Deepgram nova-2 model with diarization for speaker separation.
    """
    options = {
        "diarize": enable_diarization,
        "utterances": enable_utterances,
        "diarize_version": "v2",
    }
    
    return submit_audio_for_transcription(
        audio_source=meeting_audio_path,
        model=DEFAULT_MODEL,
        options=options,
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = submit_audio_for_transcription(sys.argv[1])
        print(f"Request ID: {result['request_id']}")
        print(f"Provider: {result['provider']}")
        print(f"Status: {result['status']}")
    else:
        print("Usage: python submit_transcription.py <audio_url_or_path>")
