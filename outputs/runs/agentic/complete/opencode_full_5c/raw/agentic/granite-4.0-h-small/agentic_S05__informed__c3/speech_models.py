# Local request, response, and normalization helpers for Streaming Speech-to-Text
# This module contains request builders, response parsers, and text normalization utilities

from typing import Any, Dict, List

# Amazon Transcribe Streaming request format
# Request is a dict sent via websocket
Request = Dict[str, Any]

# Example of building a Transcribe streaming request with language settings


def build_transcribe_stream_request(model: str) -> Request:
    """Create a request dict for Amazon Transcribe Streaming.","""
    return {
        "RequestType": "StartStreamTranscription",
        "LanguageCode": model,
        "MediaEncoding": "pcm",
        "SampleRate": 16000,
        "EnableChannelIdentification": False,
        "VocabularyName": None,  # optional custom vocab
    }


# Normalization utilities for transcripts
import re


def normalize_transcript(text: str) -> str:
    """Basic normalization: trim, collapse whitespace, lower case.","""
    text = text.strip()
    text = re.sub(r"\\s+", " ", text)
    return text.lower()


# Placeholder definitions for other providers
# Alibaba Cloud Speech response model (example)
AlibabaResponse = Dict[str, Any]


def parse_alibaba_speech_response(resp: AlibabaResponse) -> str:
    """Extract partial transcript from Alibaba response.","""
    # Adjust field names to provider's actual structure
    return resp.get("partial_transcript", "")


# Watson STT WebSocket response model (example)
WatsonResponse = Dict[str, Any]


def parse_watson_stt_response(resp: WatsonResponse) -> str:
    """Extract interim text from Watson WebSocket message.","""
    return (
        resp.get("results", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
    )


# Dummy definitions for completeness
GoogleResponse = Dict[str, Any]
OpenAiResponse = Dict[str, Any]
DeeplResponse = Dict[str, Any]

# Normalization for model outputs if needed


def postprocess_transcript(provider: str, text: str) -> str:
    """Run provider-specific post-processing before returning final result.","""
    if provider == "amazon":
        # Transcribe may insert extra markers; strip them
        return normalize_transcript(text)
    elif provider == "google":
        return normalize_transcript(text)
    return text
