import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def check_safety(text_content: str):
    """Checks text content for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Provider-specific categories and thresholds can be configured
    request = AnalyzeTextOptions(
        text=text_content,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE],
        blocklist_names=["MyBlocklist"], # Example blocklist, replace or remove
        halt_on_blocklist_hit=True,
    )

    try:
        response = client.analyze_text(request)
        safety_results = {}
        for category in response.categories_analysis:
            safety_results[category.category.value] = {
                "severity": category.severity,
                "detected": category.severity > 0 # Severity 0 usually means no detection
            }
        # Also check blocklist matches if any
        if response.blocklist_matches:
            safety_results["blocklist_matches"] = [{
                "blocklist_name": match.blocklist_name,
                "block_item_text": match.block_item_text,
                "block_item_id": match.block_item_id
            } for match in response.blocklist_matches]
        return safety_results
    except Exception as e:
        print(f"Error analyzing text for safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage with placeholder environment variables
    # Make sure to set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    test_text = "I hate this! This is terrible and I want to hurt someone."
    # test_text = "This is a perfectly safe sentence."
    safety_output = check_safety(test_text)
    print(f"Content Safety Analysis: {safety_output}")
