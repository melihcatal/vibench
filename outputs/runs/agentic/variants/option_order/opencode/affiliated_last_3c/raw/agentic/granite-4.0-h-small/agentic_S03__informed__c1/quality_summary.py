import os
from ibm_watsonx_ai.identity import APIClient
from ibm_watsonx_ai.main_services.language import TranslationService
from ibm_cloud_sdk_core import ApiException

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'watsonx')
if PROVIDER_NAME != 'watsonx':
    raise ValueError('QualitySummary works only with watsonx.ai for this example')

# Set up authentication (API key and project ID)
api_key = os.getenv('WATSONX_API_KEY')
project_id = os.getenv('WATSONX_PROJECT_ID')
api_client = APIClient(api_key=api_key)
translation = TranslationService(api_client, project_id=project_id)

def summarize_quality(translated_texts):
    """Summarize translation quality issues using watsonx.ai guardrails.",
    issues = []
    for text in translated_texts:
        try:
            # Simple call to get safety score (placeholder logic)
            response = translation.check_content(text=text, content_filter=['profanity','toxicity'])
            if response.get('score', 0) < 0.5:
                issues.append({'text': text, 'issue': 'low quality', 'score': response['score']})
        except ApiException as e:
            issues.append({'text': text, 'issue': 'api_error', 'details': str(e)})
    return issues