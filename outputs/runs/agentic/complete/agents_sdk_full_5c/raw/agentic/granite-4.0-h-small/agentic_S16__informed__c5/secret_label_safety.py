import json
from typing import List

from watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.auth import BearerTokenAuth

from security_client import get_config
from security_models import SecretDef

def secret_label_safety(secret_def: SecretDef, labels: List[str], notes: List[str]) -> bool:
    """Check secret labels and notes for unsafe content using watsonx guardrails / HAP detection.
    Returns True if safe, False otherwise.
    """
    auth = BearerTokenAuth(token=os.getenv('WATSONX_API_KEY'))  # basic auth example
    auth.configure_http()  # optional for some services (not required for ai.text)
    client = WatsonxAiClient(auth=auth, project_id=os.getenv('WATSONX_PROJECT_ID'))
    content = labels + notes
    # Using the NLP moderation endpoint (text content safety)
    response = client.nlp.moderation(text=content, model_id='en-safety')
    # response.structure contains a list of moderation results per text
    for result in response.structure:
        if result.detected:
            return False  # unsafe content detected
    return True
