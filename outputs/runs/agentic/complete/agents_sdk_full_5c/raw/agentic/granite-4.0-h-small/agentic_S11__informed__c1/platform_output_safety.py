import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from model_client import ManagedModelClient

def platform_output_safety(output_text: str) -> bool:
    """Check model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Content Safety credentials not configured')
    client = ContentSafetyClient(endpoint=endpoint, credential_key=key)
    analysis = client.analyze_text(AnalyzeTextOptions(text=output_text))
    # The SDK returns a flag indicating if content is flagged as unsafe
    return analysis.flagged_content is False
