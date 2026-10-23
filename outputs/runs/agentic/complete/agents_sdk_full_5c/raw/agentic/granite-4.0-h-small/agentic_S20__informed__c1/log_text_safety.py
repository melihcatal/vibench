import os
import json
from google.cloud import content_safety

def check_safety(log_entry: dict, safe_content_type: str = 'TEXT_PII') -> bool:
    """Scans log entry text for unsafe content using Google Cloud Content Safety.

    Args:
        log_entry (dict): Log payload with a 'message' key.
        safe_content_type (str): Type of unsafe content to detect.
    Returns:
        True if safe, False if unsafe content detected.
    """
    client = content_safety.ContentSafetyClient()
    parent = 'projects/my-project'  # Project where CM API is enabled
    response = client.check_text(request={
        'parent': parent,
        'type': safe_content_type,
        'text': log_entry.get('message', '')
    })
    # Response includes .safe field (bool)
    return response.safe

# Example usage (remove for library)
if __name__ == '__main__':
    sample = {'message': 'Enter your credit card number: 1234 5678 9012 3456'}
    print('Safe?', check_safety(sample))
