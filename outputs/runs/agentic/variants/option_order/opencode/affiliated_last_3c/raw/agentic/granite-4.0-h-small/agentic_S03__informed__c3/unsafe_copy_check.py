import os

try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.ai.contentsafety.models import TextContent
except ImportError:
    raise ImportError(
        "Install Azure Content Safety SDK: pip install azure-ai-contentsafety"
    )

# Load environment variables (Azure)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
if not (AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY):
    raise RuntimeError("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY")


def check_unsafe_copy(translated_texts: list[str]) -> list[bool]:
    """Check localized copy for unsafe content using Azure Content Safety.

    Args:
        translated_texts (list[str]): List of translated strings.

    Returns:
        list[bool]: List indicating unsafe (True) vs safe (False) content per entry.
    """
    credentials = DefaultAzureCredential()
    client = ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT, credential=credentials
    )
    results = []
    for text in translated_texts:
        response = client.analyze_content(TextContent(text=text))
        # Assume unsafe if the model flags any harm
        unsafe = any(flag.detected for flag in response.flags)
        results.append(unsafe)
    return results
