import os
import requests
from google.cloud import dlp_v2

# Service identifier:
# Provider: Google Cloud DLP (text content safety)

API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # JSON path for service account
c def check_safety(text: str) -> bool:
    """Check extracted document text for unsafe content using Google DLP.

    Args:
        text: raw OCR string.

    Returns:
        True if safe, False otherwise.
    """
    client = dlp_v2.DlpServiceClient()
    # Define info types to detect (e.g., PERSON, EMAIL_ADDRESS)
    info_types = [{'name': 'PERSON'}, {'name': 'EMAIL_ADDRESS'}]
    # Create inspect configuration
    inspect_config = {'info_types': info_types, 'include_quote': True}
    # Create content item
    item = {'value': text}
    # Call DLP API
    response = client.inspect_content(request={'inspect_config': inspect_config, 'item': item})
    # If findings are empty, consider text safe
    return len(response.result.findings) == 0
