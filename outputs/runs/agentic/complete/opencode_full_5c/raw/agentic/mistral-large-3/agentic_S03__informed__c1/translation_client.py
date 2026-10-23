import os
from typing import Dict, List, Optional

import boto3
from botocore.config import Config


class TranslationClient:
    """
    Client helper for Amazon Translate with configuration and utility methods.
    """

    def __init__(
        self,
        region: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        """
        Initializes the Amazon Translate client.

        Args:
            region: AWS region (e.g., 'us-east-1').
            max_retries: Maximum number of retries for API calls.
            timeout: Timeout in seconds for API calls.
        """
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.config = Config(
            retries={"max_attempts": max_retries},
            connect_timeout=timeout,
            read_timeout=timeout,
        )
        self.client = boto3.client(
            "translate", region_name=self.region, config=self.config
        )

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """
        Retrieves the list of supported languages for translation.

        Returns:
            List of dictionaries with language codes and names.
        """
        try:
            response = self.client.list_languages()
            return response.get("Languages", [])
        except Exception as e:
            raise ValueError(f"Failed to fetch supported languages: {e}")

    def validate_language_pair(self, source_lang: str, target_lang: str) -> bool:
        """
        Validates if the language pair is supported by Amazon Translate.

        Args:
            source_lang: The source language code (e.g., 'en').
            target_lang: The target language code (e.g., 'es').

        Returns:
            True if the language pair is supported, False otherwise.
        """
        try:
            languages = self.get_supported_languages()
            supported_codes = {lang["LanguageCode"] for lang in languages}
            return source_lang in supported_codes and target_lang in supported_codes
        except Exception:
            return False
