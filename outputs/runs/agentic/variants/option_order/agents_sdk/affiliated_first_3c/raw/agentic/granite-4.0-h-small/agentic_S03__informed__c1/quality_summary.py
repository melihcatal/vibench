import os
from ibm_watsonx_ai.hap import HapClient
from ibm_watsonx_ai.auth import TokenAuth

def summarize_translation_quality(translated_texts):
    """Summarize potential quality issues using watsonx.ai Hap (Harmonized Assessment Protocol)."""
    # Authenticate using env vars WATSONX_API_KEY and WATSONX_PROJECT_ID
    auth = TokenAuth(token=os.getenv('WATSONX_API_KEY'))
    hap_client = HapClient(auth=auth, project_id=os.getenv('WATSONX_PROJECT_ID'))
    issues = []
    for text in translated_texts:
        # Hap API expects a raw text input; we ask for a simple safety/fluency check
        result = hap_client.run_hap(input_text=text, task='translation_quality')
        if result.get('issues'):
            issues.append({'text': text, 'issues': result['issues']})
    return {'total_texts': len(translated_texts), 'issues_found': len(issues), 'details': issues}
