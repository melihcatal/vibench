import os, json
from ibm_watsonx_ai import WatsonxClient

def moderate_profile(user_id, profile_text):
    # IBM watsonx Guardrails - safetynet detection API
    client = WatsonxClient(apikey=os.getenv('WATSONX_API_KEY'), url='https://us-south.ml.cloud.ibm.com')
    response = client.safetynet.detect(text=profile_text)
    if response.get('results')[0].get('classification') == 'Risky':
        raise ValueError('Profile text contains disallowed content')
    return 'Safe'
