from typing import str
import os
from azure.ai.contentsafety import ContentSafetyClient, TextRedactionOptions
from azure.core.credentials import AzureKeyCredential
from safety_client import load_safety_config
from safety_models import default_categories

def redact_unsafe(text: str) -> str:
    config = load_safety_config()
    client = ContentSafetyClient(config[&quot;endpoint&quot;], AzureKeyCredential(config[&quot;key&quot;]))
    redaction_options = TextRedactionOptions(categories=default_categories())
    poller = client.redact_text(text, redaction_options)
    result = poller.result()
    return result.redacted_text