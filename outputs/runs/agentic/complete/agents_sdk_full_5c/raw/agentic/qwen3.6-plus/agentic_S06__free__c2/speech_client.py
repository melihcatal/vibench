"""
Local configuration and client helper utilities for Amazon Polly Text-to-Speech.

This module provides centralized configuration loading, client initialization,
and utility functions for interacting with the Amazon Polly service.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config

# Amazon Polly default configuration
POLLY_SERVICE_NAME = "polly"
POLLY_DEFAULT_REGION = os.getenv("POLLY_DEFAULT_REGION", "us-east-1")
POLLY_ENDPOINT_URL = os.getenv("POLLY_ENDPOINT_URL", None)
POLLY_VOICE_ID = os.getenv("POLLY_DEFAULT_VOICE", "Joanna")

# Supported output formats for Amazon Polly
SUPPORTED_FORMATS = ("mp3", "ogg_vorbis", "pcm")
DEFAULT_FORMAT = "mp3"


class PollyClient:
    """
    Wrapper around boto3 Polly client with configuration management.
    
    Amazon Polly service endpoint: polly.{region}.amazonaws.com
    """

    def __init__(
        self,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ):
        self.region = region_name or POLLY_DEFAULT_REGION
        self.endpoint = endpoint_url or POLLY_ENDPOINT_URL
        
        session_config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
            connect_timeout=10,
            read_timeout=30,
        )
        
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=aws_session_token or os.getenv("AWS_SESSION_TOKEN"),
            region_name=self.region,
        )
        
        client_kwargs = {
            "service_name": POLLY_SERVICE_NAME,
            "config": session_config,
        }
        if self.endpoint:
            client_kwargs["endpoint_url"] = self.endpoint
            
        self.client = session.client(**client_kwargs)

    def get_client(self):
        """Return the configured boto3 Polly client."""
        return self.client

    def describe_voices(self, language_code: Optional[str] = None):
        """
        List available voices from Amazon Polly.
        
        Args:
            language_code: BCP-47 language code (e.g., 'en-US', 'es-ES')
            
        Returns:
            boto3 response containing voice metadata
        """
        kwargs = {}
        if language_code:
            kwargs["LanguageCode"] = language_code
        return self.client.describe_voices(**kwargs)

    def synthesize_speech(
        self,
        text: str,
        voice_id: str,
        output_format: str = DEFAULT_FORMAT,
        text_type: str = "text",
        speech_rate: Optional[str] = None,
        language_code: Optional[str] = None,
    ):
        """
        Synthesize speech using Amazon Polly.
        
        Args:
            text: Plain text or SSML to synthesize
            voice_id: Amazon Polly voice ID (e.g., 'Joanna', 'Matthew')
            output_format: 'mp3', 'ogg_vorbis', or 'pcm'
            text_type: 'text' or 'ssml'
            speech_rate: Optional SSML prosody rate if not using SSML directly
            language_code: BCP-47 language code
            
        Returns:
            boto3 response with AudioStream
        """
        kwargs = {
            "Text": text,
            "VoiceId": voice_id,
            "OutputFormat": output_format,
            "TextType": text_type,
        }
        if language_code:
            kwargs["LanguageCode"] = language_code
            
        return self.client.synthesize_speech(**kwargs)


def get_polly_client() -> PollyClient:
    """Factory function to create a configured PollyClient."""
    return PollyClient()
