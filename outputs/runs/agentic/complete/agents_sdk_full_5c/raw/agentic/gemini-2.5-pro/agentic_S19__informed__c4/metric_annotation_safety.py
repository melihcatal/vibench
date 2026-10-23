import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_annotation_safety(text_annotation: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using
    Azure AI Content Safety.

    Args:
        text_annotation: The string to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_annotation, categories=[
        TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"HTTP error during analysis: {e.message}"}

    results = {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
        "is_safe": all(r.severity == 0 for r in [
            response.hate_result, 
            response.self_harm_result, 
            response.sexual_result, 
            response.violence_result
        ])
    }
    return results

if __name__ == '__main__':
    safe_note = "Investigating CPU spike on web-tier after new deployment."
    unsafe_note = "This server is garbage and should be decommissioned."

    print(f"Checking safe annotation: '{safe_note}'")
    safe_result = check_annotation_safety(safe_note)
    print(f"Result: {safe_result}\n")

    print(f"Checking unsafe annotation: '{unsafe_note}'")
    unsafe_result = check_annotation_safety(unsafe_note)
    print(f"Result: {unsafe_result}")
