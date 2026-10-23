import os

# Choose ONE concrete moderation service and keep its auth env vars.
# Example: Azure Content Safety (rest SDK)
# from azure.ai.contentsafety import ContentSafetyClient
# client = ContentSafetyClient(os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'), credential=AzureKeyCredential(os.getenv('AZURE_CONTENT_SAFETY_KEY')))

# Example: Google Gemini guardrails via watsonx.ai (SDK)
# from ibm_watsonx_ai import APIClient
# from ibm_watsonx_ai.consts import ServiceType
# client = APIClient(instance_url=os.getenv('WATSONX_ENDPOINT'), api_key=os.getenv('WATSONX_API_KEY'))
# guardrails = client.service(ServiceType.GUARDRAILS)

# For illustration we use the OpenAI moderation endpoint (rest)
import httpx
openai_api_key = os.getenv('OPENAI_API_KEY')

def check_safe(text: str) -> bool:
    """Call a hosted moderation API to detect unsafe content.

    Args:
        text (str): User‑generated text to evaluate.

    Returns:
        bool: True if safe, False if flagged as unsafe.
    """
    response = httpx.post(
        "https://api.openai.com/v1/moderations",
        json={"input": text},
        headers={"Authorization": f"Bearer {openai_api_key}"},
    )
    data = response.json()
    # OpenAI returns an array of categories; safe when none are flagged
    flags = data["results"][0]["categories"]
    return all(not flag["flagged"] for flag in flags)}