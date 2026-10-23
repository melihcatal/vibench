import os

# Choose one of the following external providers (only one should be used per project)
# AWS Amazon Translate
# ALIBABA Alibaba Machine Translation
# DEEPL DeepL API
# GOOGLE Google Cloud Translation
# AZURE Azure AI Translator

# Example: using Google Cloud Translation (default)
PROVIDER = "google"

# Helper to create a client for the selected provider
from google.cloud import translate_v2 as translate  # type: ignore


class TranslationClient:
    """Local helper to instantiate a General Text Translation client for the configured provider.

    The provider is set via the PROVIDER constant; replace the import block above to switch providers.
    """

    @staticmethod
    def get() -> object:
        if PROVIDER == "google":
            # google-cloud-translate SDK client
            return translate.Client()
        elif PROVIDER == "amazon":
            # boto3 client for Amazon Translate
            import boto3

            return boto3.client("translate")
        else:
            raise NotImplementedError(f"Provider {PROVIDER} not implemented")
