import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from translation_models import TranslationRequest, TranslationResponse


@dataclass
class TranslationConfig:
    """Configuration for translation services."""

    provider: str = "google"  # google, aws, deepl, azure, alibaba
    timeout: int = 30
    max_retries: int = 3
    batch_size: int = 100


class TranslationClient:
    """Client helper utilities for General Text Translation."""

    def __init__(self, config: Optional[TranslationConfig] = None):
        self.config = config or TranslationConfig()
        self._clients = {}

    def get_google_client(self):
        """Get Google Cloud Translation client."""
        if "google" not in self._clients:
            from google.cloud import translate_v2 as translate

            self._clients["google"] = translate.Client()
        return self._clients["google"]

    def get_aws_client(self):
        """Get Amazon Translate client."""
        if "aws" not in self._clients:
            import boto3

            self._clients["aws"] = boto3.client(
                "translate",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
        return self._clients["aws"]

    def get_deepl_client(self):
        """Get DeepL translator client."""
        if "deepl" not in self._clients:
            import deepl

            auth_key = os.getenv("DEEPL_AUTH_KEY")
            if not auth_key:
                raise ValueError("DEEPL_AUTH_KEY environment variable is required")
            self._clients["deepl"] = deepl.Translator(auth_key)
        return self._clients["deepl"]

    def get_azure_client(self):
        """Get Azure AI Translator client."""
        if "azure" not in self._clients:
            from azure.ai.translation.text import TextTranslationClient
            from azure.core.credentials import AzureKeyCredential

            key = os.getenv("AZURE_TRANSLATOR_KEY")
            endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
            region = os.getenv("AZURE_TRANSLATOR_REGION")

            if not key or not endpoint:
                raise ValueError("Azure Translator credentials not configured")

            credential = AzureKeyCredential(key)
            self._clients["azure"] = TextTranslationClient(
                endpoint=endpoint, credential=credential, region=region
            )
        return self._clients["azure"]

    def normalize_language_code(self, lang_code: str) -> str:
        """Normalize language codes to provider-specific format."""
        # Map common language codes to provider-specific formats
        lang_map = {
            "zh": "zh-CN",
            "zh-cn": "zh-CN",
            "zh-tw": "zh-TW",
            "pt": "pt-BR",
            "pt-br": "pt-BR",
            "pt-pt": "pt-PT",
        }
        return lang_map.get(lang_code.lower(), lang_code)

    def validate_request(self, request: TranslationRequest) -> bool:
        """Validate translation request parameters."""
        if not request.text and not request.texts:
            return False

        if request.target_language and len(request.target_language) < 2:
            return False

        if request.source_language and len(request.source_language) < 2:
            return False

        return True

    def create_response(
        self,
        translated_text: Optional[str] = None,
        translated_texts: Optional[list] = None,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> TranslationResponse:
        """Create a normalized translation response."""
        return TranslationResponse(
            translated_text=translated_text,
            translated_texts=translated_texts,
            source_language=source_language,
            target_language=target_language,
            provider=provider or self.config.provider,
        )
