import os

# Local helper: configuration for Text Content Safety providers

# IBM WatsonX Guardrails (same-scenario)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Alibaba Cloud Content Moderation (same-scenario)
ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# Perspective API (same-scenario)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

# Tisane (same-scenario)
TISANE_API_KEY = os.getenv("TISANE_API_KEY")

# Azure AI Content Safety (same-scenario)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def get_client(provider: str):
    """Return a provider‑specific client helper based on name.

    Parameters
    ----------
    provider: str
        One of "watsonx", "alibaba", "perspective", "tisane", "azure".
    """
    if provider == "watsonx":
        from ibm_watsonx_ai import WatsonxClient

        return WatsonxClient(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
    elif provider == "alibaba":
        from alibabacloud_green import GreenClient

        return GreenClient(
            endpoint="green.cn-hangzhou.aliyuncs.com",
            access_key_id=ALIBABA_ACCESS_KEY_ID,
            access_key_secret=ALIBABA_ACCESS_KEY_SECRET,
        )
    elif provider == "perspective":
        import requests

        return requests.Session()
    elif provider == "tisane":
        import requests

        return requests.Session()
    elif provider == "azure":
        from azure.ai.contentsafety import ContentSafetyClient
        from azure.core.credentials import AzureKeyCredential

        return ContentSafetyClient(
            endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
            credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY),
        )
    else:
        raise ValueError(f"Unknown provider {provider}")
