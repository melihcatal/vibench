import os

# General configuration for various translation providers


def get_provider_config(provider: str) -> dict:
    """Return configuration dict suitable for the chosen provider.

    Supported providers:
        'deepl', 'google', 'azure', 'amazon', 'alibaba'
    """
    config = {}
    if provider == "deepl":
        config = {
            "service": "DeepL API",
            "sdk": "deepl",
            "interface": "sdk",
            "auth_env": "DEEPL_AUTH_KEY",
        }
    elif provider == "google":
        config = {
            "service": "Cloud Translation",
            "sdk": "google-cloud-translate",
            "interface": "sdk",
            "auth_env": "GOOGLE_APPLICATION_CREDENTIALS",
        }
    elif provider == "azure":
        config = {
            "service": "Azure AI Translator",
            "sdk": "azure-ai-translation-text",
            "interface": "sdk_or_rest",
            "auth_env": ["AZURE_TRANSLATOR_KEY", "AZURE_TRANSLATOR_REGION"],
        }
    elif provider == "amazon":
        config = {
            "service": "Amazon Translate",
            "sdk": "boto3",
            "interface": "sdk",
            "auth_env": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        }
    elif provider == "alibaba":
        config = {
            "service": "Alibaba Machine Translation",
            "sdk": "alibabacloud_alimt",
            "interface": "sdk",
            "auth_env": [
                "ALIBABA_CLOUD_ACCESS_KEY_ID",
                "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
            ],
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    return config


def load_auth_token(provider: str) -> str:
    """Load the authentication token/environment variable for the given provider."""
    cfg = get_provider_config(provider)
    if isinstance(cfg["auth_env"], list):
        # Multiple env vars, at least one must be set
        for env in cfg["auth_env"]:
            val = os.getenv(env)
            if val:
                return val
        raise EnvironmentError(
            f"None of the required auth env vars set for {provider}: {cfg['auth_env']}"
        )
    else:
        token = os.getenv(cfg["auth_env"])
        if not token:
            raise EnvironmentError(
                f"Auth env var not set for {provider}: {cfg['auth_env']}"
            )
        return token


def normalize_request(payload: dict, provider: str) -> dict:
    """Normalize request payload to provider-specific format.

    This is a stub that can be extended per provider.
    """
    if provider == "deepl":
        # DeepL expects 'text' and 'source_lang', 'target_lang'
        return {
            "text": payload["text"],
            "source_lang": payload["source_lang"].upper(),
            "target_lang": payload["target_lang"].upper(),
        }
    if provider == "google":
        # Google expects 'q', 'source', 'target', 'format'
        return {
            "q": payload["text"],
            "source": payload["source_lang"].lower(),
            "target": payload["target_lang"].lower(),
            "format": "html",  # default
        }
    if provider == "azure":
        # Azure expects 'documents' list with 'text' and 'language'
        return {
            "documents": [{"text": payload["text"], "language": payload["source_lang"]}]
        }
    if provider == "amazon":
        # Boto3 expects a list of texts and source/target
        return {
            "Texts": [payload["text"]],
            "SourceLanguageCode": payload["source_lang"],
            "TargetLanguageCode": payload["target_lang"],
        }
    if provider == "alibaba":
        # Alibaba expects 'SourceText', 'SourceLanguage', 'TargetLanguage'
        return {
            "SourceText": payload["text"],
            "SourceLanguage": payload["source_lang"].lower(),
            "TargetLanguage": payload["target_lang"].lower(),
        }
    raise ValueError(f"Normalization for provider {provider} not implemented")
