import os
from ibm_watsonx_ai import WatsonXAI
from typing import Dict

def translate_runbook_note(note: str, target_lang: str = "es") -> str:
    """Translate a secret‑rotation runbook note using watsonx.ai translation.
    Args:
        note: The source text (usually English). 
        target_lang: Target language code (e.g., 'es' for Spanish).
    Returns:
        Translated text.
    """
    wx = WatsonXAI()
    translation = wx.translate_text(text=note, target_lang=target_lang)
    return translation["translation"]

if __name__ == "__main__":
    # Example: translate a runbook snippet stored as a secret
    runbook_secret = "rotation-runbook-notes"
    # Retrieve the note (using security_client.py, omitted here for brevity)
    # For illustration we embed a static string
    sample_note = "Rotate the database secret every 90 days and record the version ID."
    translated = translate_runbook_note(sample_note)
    print(f"Translated note: {translated}")