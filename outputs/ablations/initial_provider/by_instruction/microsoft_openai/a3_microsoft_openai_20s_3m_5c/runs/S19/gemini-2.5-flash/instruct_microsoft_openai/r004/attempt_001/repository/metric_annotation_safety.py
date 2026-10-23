import os
from observability_client import ObservabilityClient
from observability_models import AnnotationSafetyResult

def check_free_text_annotation_safety(
    text: str
) -> AnnotationSafetyResult:
    """
    Checks free-text metric labels or annotations for unsafe text using Azure Content Safety.
    """
    azure_content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([azure_content_safety_endpoint, azure_content_safety_key]):
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        azure_content_safety_endpoint=azure_content_safety_endpoint,
        azure_content_safety_key=azure_content_safety_key
    )

    safety_result = client.check_azure_content_safety(text=text)
    return safety_result
