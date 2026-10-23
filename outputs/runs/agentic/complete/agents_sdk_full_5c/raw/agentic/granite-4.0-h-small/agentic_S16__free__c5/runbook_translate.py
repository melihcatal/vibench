# [LATER-STEP] runbook_translate.py
from security_models import SecretReference
import json

def translate_runbook(secret: SecretReference, runbook_text: str) -> str:
    """Translate secret‑rotation runbook notes into a concise runbook summary.

    Args:
        secret (SecretReference): The secret whose runbook we are translating.
        runbook_text (str): Full runbook content (plain text).

    Returns:
        str: Summarized runbook instructions.
    """
    # Placeholder: run a translation or summarization model in a real implementation
    # For demo, just return the first sentence.
    if not runbook_text.strip():
        return "No runbook provided"
    return runbook_text.split('.')[0] + "."
