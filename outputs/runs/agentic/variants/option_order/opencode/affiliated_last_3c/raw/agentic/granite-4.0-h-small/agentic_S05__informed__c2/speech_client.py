# [HELPER] speech_client.py
# Provides local configuration and client utilities for Streaming Speech-to-Text
# This example abstracts provider-specific instantiation

# Generic configuration loader
import os

# Example: load environment variables for specific providers
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")

# Helper for creating provider-specific clients
# Add new providers by extending this dictionary with configuration parameters
PROVIDERS = {
    "deepgram": {"client": None, "required": ["DEEPGRAM_API_KEY"]},
    "amazon": {
        "client": None,
        "required": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
    },
    "google": {"client": None, "required": ["GOOGLE_APPLICATION_CREDENTIALS"]},
    "azure": {"client": None, "required": ["AZURE_SPEECH_KEY"]},
}

# Example: initialize a provider client
# def initialize_provider(provider_name):
#     cfg = PROVIDERS.get(provider_name.lower())
#     if not cfg:
#         raise ValueError(f"Unknown provider: {provider_name}")
#     missing = [var for var in cfg["required"] if not os.getenv(var)]
#     if missing:
#         raise RuntimeError(f"Missing env vars for {provider_name}: {missing}")
#     # Instantiate client here (e.g., deepgram SDK, boto3, etc.)
#     pass

# This module would be imported by scenario files
