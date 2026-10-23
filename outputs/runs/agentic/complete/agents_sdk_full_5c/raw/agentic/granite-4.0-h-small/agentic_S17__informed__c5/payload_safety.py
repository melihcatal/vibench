import json
import re
from google.cloud import dlp_v2 as dlp

from security_models import DecryptRequest

def payload_safety(decrypted_text: str) -> bool:
    """Checks a decrypted payload for unsafe or potentially disallowed content.

    Uses Google Cloud DLP's content inspection for PII, profanity, and
    custom regex patterns.
    Returns True if content is safe, otherwise False.
    """
    client = dlp.DlpServiceClient()
    # Define inspection config: PII, profanity, and a regex for credit card numbers
    inspect_config = dlp.InspectConfig(
        info_types=[
            dlp.InfoType(name='PII'),
            dlp.InfoType(name='PROFANITY'),
        ],
        custom_info_types=[
            {
                'regex': {
                    'pattern': r'\\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\\b'
                },
                'info_type': {
                    'name': 'CREDIT_CARD_NUMBER'
                }
            }
        ],
        include_quote=True,
    )
    # Prepare input item
    item = dlp.ContentItem(text=decrypted_text)
    # Run inspection
    response = client.inspect_content(dlp.InspectContentRequest(
        parent='projects/PROJECT_ID/locations/global',
        inspect_config=inspect_config,
        item=item,
    ))
    # If any findings, consider unsafe
    return len(response.result.findings) == 0
