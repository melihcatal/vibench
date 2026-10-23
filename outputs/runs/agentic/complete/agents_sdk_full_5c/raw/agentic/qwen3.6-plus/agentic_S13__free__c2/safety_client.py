"""
safety_client.py - Local configuration and client helper utilities for Text Content Safety.

Provides configuration loading, client instantiation, and retry logic for the
OpenAI Moderation API (api.openai.com).
"""

import os
import time
import openai


DEFAULT_MODEL = "text-moderation-latest"
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


class SafetyClientConfig:
    """Configuration holder for OpenAI moderation client."""

    def __init__(
        self,
        api_key: str = None,
        model: str = DEFAULT_MODEL,
        api_base: str = DEFAULT_API_BASE,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        timeout: int = 30,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.api_base = api_base
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI Moderation API access")
        return True

    def to_dict(self) -> dict:
        """Return configuration as dictionary (excluding API key)."""
        return {
            "model": self.model,
            "api_base": self.api_base,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "timeout": self.timeout,
            "provider": "openai",
            "provider_endpoint": "api.openai.com",
        }


def load_config_from_env() -> SafetyClientConfig:
    """
    Load SafetyClientConfig from environment variables.

    Expected environment variables:
        OPENAI_API_KEY: Required API key
        OPENAI_MODERATION_MODEL: Optional model override
        OPENAI_API_BASE: Optional API base URL
        SAFETY_MAX_RETRIES: Optional max retry count
        SAFETY_RETRY_DELAY: Optional retry delay in seconds
        SAFETY_TIMEOUT: Optional timeout in seconds

    Returns:
        Configured SafetyClientConfig instance.
    """
    return SafetyClientConfig(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model=os.environ.get("OPENAI_MODERATION_MODEL", DEFAULT_MODEL),
        api_base=os.environ.get("OPENAI_API_BASE", DEFAULT_API_BASE),
        max_retries=int(os.environ.get("SAFETY_MAX_RETRIES", DEFAULT_MAX_RETRIES)),
        retry_delay=float(os.environ.get("SAFETY_RETRY_DELAY", DEFAULT_RETRY_DELAY)),
        timeout=int(os.environ.get("SAFETY_TIMEOUT", 30)),
    )


def create_moderation_client(config: SafetyClientConfig = None) -> openai.OpenAI:
    """
    Create an OpenAI client for moderation API calls.

    Args:
        config: Optional SafetyClientConfig. If None, loads from environment.

    Returns:
        Configured openai.OpenAI client instance.
    """
    if config is None:
        config = load_config_from_env()

    config.validate()

    client = openai.OpenAI(
        api_key=config.api_key,
        base_url=config.api_base,
        timeout=config.timeout,
        max_retries=config.max_retries,
    )

    return client


def moderate_with_retry(
    client: openai.OpenAI,
    text: str,
    model: str = DEFAULT_MODEL,
    max_retries: int = DEFAULT_MAX_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> dict:
    """
    Call the OpenAI Moderation API with retry logic for transient errors.

    Args:
        client: OpenAI client instance.
        text: Text to moderate.
        model: Moderation model to use.
        max_retries: Maximum number of retry attempts.
        retry_delay: Delay between retries in seconds.

    Returns:
        Moderation API response as dictionary.

    Raises:
        openai.APIError: If all retries are exhausted.
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            result = client.moderations.create(
                input=text,
                model=model,
            )
            return {
                "flagged": result.results[0].flagged,
                "category_scores": {
                    cat: getattr(result.results[0].category_scores, cat, 0.0)
                    for cat in SAFETY_CATEGORIES
                },
                "model": model,
                "provider": "openai",
                "provider_endpoint": "api.openai.com/v1/moderations",
            }
        except (openai.APIConnectionError, openai.RateLimitError, openai.APITimeoutError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))

    raise last_exception


def batch_moderate_with_retry(
    client: openai.OpenAI,
    texts: list[str],
    model: str = DEFAULT_MODEL,
    max_retries: int = DEFAULT_MAX_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> list[dict]:
    """
    Call the OpenAI Moderation API for a batch of texts with retry logic.

    Args:
        client: OpenAI client instance.
        texts: List of texts to moderate.
        model: Moderation model to use.
        max_retries: Maximum number of retry attempts.
        retry_delay: Delay between retries in seconds.

    Returns:
        List of moderation results, one per input text.
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            result = client.moderations.create(
                input=texts,
                model=model,
            )

            batch_results = []
            for idx, mod_result in enumerate(result.results):
                batch_results.append({
                    "index": idx,
                    "flagged": mod_result.flagged,
                    "category_scores": {
                        cat: getattr(mod_result.category_scores, cat, 0.0)
                        for cat in SAFETY_CATEGORIES
                    },
                    "model": model,
                    "provider": "openai",
                })

            return batch_results

        except (openai.APIConnectionError, openai.RateLimitError, openai.APITimeoutError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))

    raise last_exception


def get_provider_info() -> dict:
    """
    Return provider identification information for logging/auditing.

    Returns:
        Dictionary with OpenAI provider details.
    """
    return {
        "provider": "openai",
        "provider_name": "OpenAI",
        "api_endpoint": "api.openai.com/v1/moderations",
        "model": DEFAULT_MODEL,
        "api_version": "v1",
        "documentation_url": "https://platform.openai.com/docs/guides/moderation",
    }
