DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Summarize onboarding state for support using watsonx.ai guardrails / HAP detection

---

```python
import os
from ibm_watsonx_ai.services import LanguageService
from ibm_watsonx_ai.auth import get_authenticator_from_environment

# Load watsonx credentials from env vars
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

# Authenticate with watsonx
authenticator = get_authenticator_from_environment(service_name='language')
language_service = LanguageService(authenticator=authenticator, service_url='https://api-us-south.watsonx.ai')

def summarize_onboarding(onboarding_notes: str) -> str:
    """Use watsonx Language Service to create a concise support summary.
    Returns a plain-text summary.
    """
    # Simple prompt to the LLM for summarization
    prompt = f"Summarize the following onboarding notes in one sentence:\n\n{onboarding_notes}\n"
    response = language_service.chat(
        system="You are an AI assistant summarizing user onboarding data for support.",
        messages=[{"role": "user", "text": prompt}]
    )
    return response['choices'][0]['message']['content']
```