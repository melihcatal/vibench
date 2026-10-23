import json
from safety_check_client import SafetyClient
from safety_models import SafetyResult

def visual_safety_text(analysis_text: str) -> bool:
    """Check generated visual labels for unsafe text using Azure AI Content Safety service before publishing."""
    client = SafetyClient()
    verdict = client.check_text(analysis_text)
    return verdict.is_safe
