# Local configuration and client utilities for Streaming Speech-to-Text
# This module abstracts provider-specific auth and initialization

import os

# Amazon Transcribe Streaming client helper
# SDK: boto3 (transcribe streaming)
# Service: Amazon Transcribe Streaming

# Configurable env vars (set before running)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def get_amazon_transcribe_streaming_client() -> any:
    """Return a pre-configured Transcribe Streaming client (boto3)."""
    import boto3

    transcribe = boto3.client(
        "transcribe-streaming",
        region_name="us-east-1",  # adjust as needed
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    return transcribe


# DashScope Real-time ASR client helper
# SDK: dashscope
# Service: DashScope Real-time speech recognition


def get_dashscope_asr_client() -> any:
    """Return a configured DashScope SpeechRecognizer client."""
    import dashscope

    client = dashscope.speech.SpeechRecognizer(
        api_key=os.getenv("DASHSCOPE_API_KEY"), model="general"
    )
    return client


# Cloud Speech-to-Text streaming client helper
# SDK: google-cloud-speech
# Service: Google Cloud Speech-to-Text streaming


def get_google_cloud_speech_client() -> any:
    """Return a configured Google Speech client for streaming.
    Requires GOOGLE_APPLICATION_CREDENTIALS env pointing to JSON key file.
    """
    from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()
    return client


# Azure Speech Streaming client helper
# SDK: azure-cognitiveservices-speech
# Service: Azure AI Speech streaming


def get_azure_speech_client() -> any:
    """Return an Azure SpeechConfig with subscription key and region.
    Uses AZURE_SPEECH_KEY and AZURE_SPEECH_REGION env vars.
    """
    from azure.cognitiveservices.speech import SpeechConfig

    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    audio_config = speech.AudioConfiguration()
    return speech_config


# IBM Watson STT WebSocket client helper
# SDK: ibm-watson
# Service: Watson Speech to Text WebSocket


def get_watson_stt_websocket_client() -> any:
    """Return a Watson SpeechToTextV1 client for use with WebSocket streaming.
    Requires IBM_STT_APIKEY and IBM_STT_URL env vars.
    """
    from ibm_watson import SpeechToTextV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
    client = SpeechToTextV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_STT_URL"))
    return client
