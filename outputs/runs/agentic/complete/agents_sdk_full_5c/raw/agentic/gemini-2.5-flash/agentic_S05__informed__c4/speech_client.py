import os

def get_google_speech_client_config():
    """
    Provides configuration for Google Cloud Speech-to-Text client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    """
    return {
        "sample_rate_hertz": 16000,
        "language_code": "en-US",
        "enable_automatic_punctuation": True,
        "interim_results": True,
    }

def get_azure_speech_client_config():
    """
    Provides configuration for Azure AI Speech client.
    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set for Azure Speech.")
    return {
        "subscription_key": speech_key,
        "service_region": speech_region,
        "speech_recognition_language": "en-US",
    }

def get_deepgram_client_config():
    """
    Provides configuration for Deepgram client.
    Requires DEEPGRAM_API_KEY environment variable.
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY must be set for Deepgram.")
    return {
        "api_key": api_key,
        "language": "en-US",
        "punctuate": True,
        "interim_results": True,
        "smart_format": True,
    }

def get_aws_transcribe_client_config():
    """
    Provides configuration for AWS Transcribe Streaming client.
    Requires AWS credentials to be configured (e.g., via environment variables or AWS CLI).
    """
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    return {
        "region_name": aws_region,
        "language_code": "en-US",
        "media_sample_rate_hertz": 16000,
        "media_encoding": "pcm",
        "enable_automatic_punctuation": True,
    }
