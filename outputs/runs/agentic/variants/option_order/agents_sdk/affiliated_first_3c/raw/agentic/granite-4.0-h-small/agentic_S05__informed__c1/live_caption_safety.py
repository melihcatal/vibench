import requests
import json
from ibm_watsonx_ai import watsonxai

def check_safety(transcript):
    """Uses Watsonx Guardrails (HAP detection) to evaluate safety of live transcript.
    Returns a dictionary with safety flags and suggestions."
    # Example using IBM watsonx.ai Guardrails API (REST)
    api_key = os.getenv('WATSONX_API_KEY')
    project_id = os.getenv('WATSONX_PROJECT_ID')
    endpoint = 'https://api.ibm.com/watsonx/v1/guardrails/v1/check'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'text': transcript,
        'language': 'en'
    }
    resp = requests.post(endpoint, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f'Guardrails API error: {resp.status_code}')
    result = resp.json()
    # Simplify output: flag unsafe content
    unsafe = result.get('unsafe_content', False)
    suggestions = result.get('suggestions', [])
    return {'unsafe': unsafe, 'suggestions': suggestions}

# Example usage
if __name__ == '__main__':
    sample = "The product is amazing but the delivery was terrible."
    safety = check_safety(sample)
    print('Safety check:', safety)
