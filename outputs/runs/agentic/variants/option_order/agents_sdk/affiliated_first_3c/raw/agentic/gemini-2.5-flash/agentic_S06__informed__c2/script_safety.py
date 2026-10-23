import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_script_safety(script_text: str) -> dict:
    """Checks narration scripts for unsafe content using Azure AI Content Safety."""
    # Retrieve Azure Content Safety endpoint and key from environment variables
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Analyze the text for various categories of harmful content
    request = AnalyzeTextOptions(
        text=script_text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ],
        # You can also set a blocklist_names if you have custom blocklists configured
        # blocklist_names=["MyBlocklist"],
        # output_type="FourSeverityLevels"
    )

    response = client.analyze_text(request)

    safety_results = {"text": script_text, "categories_analysis": []}
    for category_analysis in response.categories_analysis:
        safety_results["categories_analysis"].append({
            "category": category_analysis.category.value,
            "severity": category_analysis.severity # Severity score from 0 to 7
        })
    return safety_results

if __name__ == "__main__":
    # Example usage (ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"

    test_script_safe = "This is a perfectly safe script about lovely flowers."
    results_safe = check_script_safety(test_script_safe)
    print(f"Safety analysis for safe script:\n{results_safe}")

    # Example of a potentially unsafe script (for demonstration, actual results vary based on content safety model)
    test_script_unsafe = "I will kill you if you don't stop. This is full of hate and violence!"
    try:
        results_unsafe = check_script_safety(test_script_unsafe)
        print(f"\nSafety analysis for potentially unsafe script:\n{results_unsafe}")
    except Exception as e:
        print(f"\nCould not analyze unsafe script (likely due to missing credentials/endpoint): {e}")
