import os
import requests
from google.cloud import dlp_v2 as dlp

def moderate_profile_text(user_id: str, profile_text: str) -> str:
    """Moderate profile text before activation using Google Cloud DLP.
    Returns sanitized text.
    """
    client = dlp.DlpServiceClient()
    # Provider identifier baked into client import (Google Cloud DLP)
    # Build inspect request
    inspect_config = {
        'info_types': [{'name': info_type} for info_type in ['NAME', 'EMAIL_ADDRESS', 'PHONE_NUMBER']]
    }
    item = {'value': profile_text}
    response = client.inspect_content(request={'inspect_config': inspect_config, 'item': item})
    findings = response.result.findings
    if findings:
        # Simple replacement: remove/replace sensitive info
        sanitized = profile_text
        for finding in findings:
            sanitized = sanitized.replace(finding.original_string, '[REDACTED]')
        return sanitized
    return profile_text

# Example usage (not executed):
# safe_text = moderate_profile_text('u123', 'Contact: alice@example.com')
# print(safe_text)
