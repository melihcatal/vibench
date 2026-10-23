from typing import Dict, Any
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import load_safety_config
from safety_models import default_categories, response_to_scores

def moderate_text(text: str) -> Dict[str, Dict[str, Any]]:
    config = load_safety_config()
    client = ContentSafetyClient(config[&quot;endpoint&quot;], AzureKeyCredential(config[&quot;key&quot;]))
    poller = client.analyze_text(text, default_categories())
    result = poller.result()
    return response_to_scores(result)