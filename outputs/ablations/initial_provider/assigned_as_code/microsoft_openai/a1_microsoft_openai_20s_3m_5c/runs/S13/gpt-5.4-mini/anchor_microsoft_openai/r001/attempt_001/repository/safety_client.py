import os

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from safety_models import SafetyConfig, normalize_text, normalize_text_list


def load_safety_config(config=None):
    config = config or {}
    return SafetyConfig(
        endpoint=config.get("endpoint") or os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
        api_key=config.get("api_key") or os.environ["AZURE_CONTENT_SAFETY_KEY"],
    )


def make_client(config=None):
    safety_config = load_safety_config(config)
    return ContentSafetyClient(safety_config.endpoint, AzureKeyCredential(safety_config.api_key))


def normalize_payload(payload):
    payload = payload or {}
    return {
        "text": normalize_text(payload.get("text")),
        "texts": normalize_text_list(payload.get("texts")),
        "thresholds": payload.get("thresholds") or {},
        "source_language": normalize_text(payload.get("source_language")),
        "target_language": normalize_text(payload.get("target_language")),
        "audio_text": normalize_text(payload.get("audio_text")),
    }
