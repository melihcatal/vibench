"""
Local configuration and client helper utilities for Batch Speech-to-Text.
Uses Deepgram as the concrete provider for transcription services.
"""

import os
import json
import logging
from typing import Optional
from deepgram import DeepgramClient, DeepgramClientOptions

logger = logging.getLogger(__name__)

DEEPGRAM_API_HOST = "api.deepgram.com"
DEFAULT_MODEL = "nova-2"


def load_deepgram_config() -> dict:
    """Load Deepgram configuration from environment or config file."""
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        config_path = os.environ.get("SPEECH_CONFIG_PATH", "speech_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                api_key = config.get("deepgram_api_key")

    if not api_key:
        raise ValueError(
            "DEEPGRAM_API_KEY environment variable or speech_config.json required"
        )

    return {
        "api_key": api_key,
        "api_url": f"https://{DEEPGRAM_API_HOST}",
        "model": os.environ.get("DEEPGRAM_MODEL", DEFAULT_MODEL),
    }


def create_deepgram_client(config: Optional[dict] = None) -> DeepgramClient:
    """
    Create and return a configured DeepgramClient instance.
    
    Provider: Deepgram (api.deepgram.com)
    SDK: deepgram-sdk
    """
    if config is None:
        config = load_deepgram_config()

    client_options = DeepgramClientOptions()
    client = DeepgramClient(api_key=config["api_key"], config=client_options)
    logger.info(f"Initialized Deepgram client for {DEEPGRAM_API_HOST}")
    return client


def get_prerecorded_client(client: DeepgramClient):
    """Get the prerecorded (batch) transcription client from Deepgram."""
    return client.listen.prerecorded.v("1")


def build_deepgram_options(
    model: str = DEFAULT_MODEL,
    diarize: bool = False,
    punctuate: bool = True,
    utterances: bool = False,
    smart_format: bool = True,
    language: str = "en",
    **kwargs,
) -> dict:
    """
    Build Deepgram API options dictionary for batch transcription.
    
    Provider-specific options for api.deepgram.com nova-2 model.
    """
    options = {
        "model": model,
        "punctuate": punctuate,
        "smart_format": smart_format,
        "language": language,
        "diarize": diarize,
        "utterances": utterances,
    }
    options.update(kwargs)
    return options
