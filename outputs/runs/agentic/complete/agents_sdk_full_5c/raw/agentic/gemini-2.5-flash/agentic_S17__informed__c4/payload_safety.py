from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import os

def check_payload_safety(text_payload: str) -> dict:
    """
    Checks decrypted text payloads for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_payload,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE],
        blocklist_names=["MyCustomBlocklist"], # Example blocklist name if you have one
        output_type="FourSeverityLevels"
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate_severity": response.hate_result.severity,
        "self_harm_severity": response.self_harm_result.severity,
        "sexual_severity": response.sexual_result.severity,
        "violence_severity": response.violence_result.severity,
        "blocklist_matches": []
    }

    if response.blocklist_matches:
        for match in response.blocklist_matches:
            safety_results["blocklist_matches"].append({
                "blocklist_name": match.blocklist_name,
                "matched_text": match.matched_text,
            })

    return safety_results

