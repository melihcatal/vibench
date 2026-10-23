import os
from google.cloud import dlp_v2 as dlp

def check_safety(script_text):
    """Use Google Cloud DLP to detect unsafe content in narration scripts.
    Args:
        script_text (str): Narration script to evaluate.
    Returns:
        bool: True if unsafe (e.g., profanity, personal data), False otherwise.
    """
    client = dlp.DlpServiceClient()
    # Configure an inspect job with common profanity and personal data info types
    inspect_config = dlp.InspectConfig(
        info_types=[
            dlp.InfoType(name='PERSON'),
            dlp.InfoType(name='EMAIL_ADDRESS'),
            dlp.InfoType(name='IP_ADDRESS'),
            dlp.InfoType(name='PHONE_NUMBER'),
            dlp.InfoType(name='PROFANITY')
        ],
        include_quote=True
    )
    # Prepare content
    item = dlp.ContentItem(text=script_text)
    # Call DLP API
    response = client.inspect_content(request={'inspect_config': inspect_config, 'item': item})
    findings = response.result.findings
    # Simple rule: if any finding is present, consider unsafe
    return len(findings) > 0
