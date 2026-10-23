from typing import Dict, Any, List
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import load_safety_config
from safety_models import default_categories, response_to_scores

def moderate_batch(texts: List[str]) -> List[Dict[str, Dict[str, Any]]]:
    config = load_safety_config()
    client = ContentSafetyClient(config[&quot;endpoint&quot;], AzureKeyCredential(config[&quot;key&quot;]))
    results = []
    for text in texts:
        poller = client.analyze_text(text, default_categories())
        result = poller.result()
        results.append(response_to_scores(result))
    return results