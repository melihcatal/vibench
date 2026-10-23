import os, json, requests

# WatsonX Guardrails API endpoint (hosted service)
GUARDRAILS_URL = 'https://api.watsonx.ibm.com/v1/guardrails'
API_KEY = os.getenv('WATSONX_API_KEY')
PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')


def check_safety(log_message: str) -> bool:
    """Run a text safety check using WatsonX Guardrails.

    Returns True if the text is deemed safe, False otherwise.
    """
    payload = {
        'text': log_message,
        'language': 'en'
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    resp = requests.post(GUARDRAILS_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    # The service returns a boolean field 'safe'
    return result.get('safe', False)

# Example usage (commented out for CI)
# if __name__ == '__main__':
#     unsafe = not check_safety('User credentials hardcoded: admin/password')
#     print('Safe:', unsafe)
