import os
from typing import Optional, Dict, Any
import json


class SafetyClient:
    """Provide local configuration and client helper utilities for Text Content Safety."""

    _instance = None

    @classmethod
    def get_client(cls) -> "SafetyClient":
        """Get singleton instance of SafetyClient."""
        if cls._instance is None:
            cls._instance = SafetyClient()
        return cls._instance

    def __init__(self):
        """Initialize safety client with configuration."""
        self.config = self._load_config()
        self._clients = {}

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment and config file."""
        config = {
            "providers": {
                "openai": {
                    "api_key": os.getenv("OPENAI_API_KEY"),
                    "moderation_model": "text-moderation-latest",
                },
                "google_perspective": {
                    "api_key": os.getenv("GOOGLE_PERSPECTIVE_API_KEY"),
                    "discovery_url": "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                },
                "azure_content_safety": {
                    "endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
                    "key": os.getenv("AZURE_CONTENT_SAFETY_KEY"),
                },
                "aws_comprehend": {
                    "region": os.getenv("AWS_REGION", "us-east-1"),
                    "access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
                    "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                },
                "anthropic": {
                    "api_key": os.getenv("ANTHROPIC_API_KEY"),
                    "model": "claude-3-opus-20240229",
                },
                "cohere": {
                    "api_key": os.getenv("COHERE_API_KEY"),
                    "model": "embed-english-v3.0",
                },
                "elevenlabs": {"api_key": os.getenv("ELEVENLABS_API_KEY")},
            },
            "default_thresholds": {
                "hate": 0.8,
                "hate/threatening": 0.8,
                "harassment": 0.8,
                "harassment/threatening": 0.8,
                "self-harm": 0.8,
                "self-harm/intent": 0.8,
                "self-harm/instructions": 0.8,
                "sexual": 0.8,
                "sexual/minors": 0.8,
                "violence": 0.8,
                "violence/graphic": 0.8,
                "TOXICITY": 0.7,
                "SEVERE_TOXICITY": 0.7,
                "IDENTITY_ATTACK": 0.7,
                "INSULT": 0.7,
                "PROFANITY": 0.7,
                "THREAT": 0.7,
            },
            "redaction_char": "*",
            "batch_size": 10,
        }

        # Try to load from config file
        config_path = os.getenv("SAFETY_CONFIG_PATH", "safety_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except Exception:
                pass

        return config

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        return self.config["providers"].get(provider, {})

    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        required_providers = [
            "openai",
            "google_perspective",
            "azure_content_safety",
            "aws_comprehend",
        ]

        for provider in required_providers:
            config = self.get_provider_config(provider)
            if provider == "openai" and not config.get("api_key"):
                return False
            elif provider == "google_perspective" and not config.get("api_key"):
                return False
            elif provider == "azure_content_safety" and not (
                config.get("endpoint") and config.get("key")
            ):
                return False
            elif provider == "aws_comprehend" and not (
                config.get("access_key_id") and config.get("secret_access_key")
            ):
                return False

        return True

    def get_default_thresholds(self) -> Dict[str, float]:
        """Get default safety thresholds."""
        return self.config["default_thresholds"]

    def get_redaction_char(self) -> str:
        """Get default redaction character."""
        return self.config.get("redaction_char", "*")

    def get_batch_size(self) -> int:
        """Get default batch size for operations."""
        return self.config.get("batch_size", 10)
