import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AssemblyAIConfig:
    api_key: str = field(
        default_factory=lambda: os.environ.get("ASSEMBLYAI_API_KEY", "")
    )
    api_base_url: str = "https://api.assemblyai.com/v2"
    polling_interval_seconds: int = 5
    max_poll_attempts: int = 300
    default_language_code: str = "en"
    default_audio_format: str = "mp3"

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")


@dataclass
class DeepLConfig:
    auth_key: str = field(default_factory=lambda: os.environ.get("DEEPL_AUTH_KEY", ""))
    api_url: str = "https://api-free.deepl.com/v2/translate"
    default_target_lang: str = "en"
    default_source_lang: str = ""

    def validate(self) -> None:
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is not set")


@dataclass
class AzureContentSafetyConfig:
    endpoint: str = field(
        default_factory=lambda: os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    )
    api_key: str = field(
        default_factory=lambda: os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    )
    api_version: str = "2024-02-15-preview"
    default_categories: list = field(
        default_factory=lambda: ["Hate", "SelfHarm", "Sexual", "Violence"]
    )

    def validate(self) -> None:
        if not self.endpoint:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is not set"
            )
        if not self.api_key:
            raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is not set")


@dataclass
class DashScopeConfig:
    api_key: str = field(
        default_factory=lambda: os.environ.get("DASHSCOPE_API_KEY", "")
    )
    default_model: str = "qwen-turbo"
    default_embedding_model: str = "text-embedding-v3"
    default_embedding_dimensions: int = 1536

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable is not set")


def load_assemblyai_config() -> AssemblyAIConfig:
    config = AssemblyAIConfig()
    config.validate()
    return config


def load_deepl_config() -> DeepLConfig:
    config = DeepLConfig()
    config.validate()
    return config


def load_azure_content_safety_config() -> AzureContentSafetyConfig:
    config = AzureContentSafetyConfig()
    config.validate()
    return config


def load_dashscope_config() -> DashScopeConfig:
    config = DashScopeConfig()
    config.validate()
    return config
