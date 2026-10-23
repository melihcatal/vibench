import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of a given text using Azure AI Content Safety.
    This helps in moderating content before it's embedded or used.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Categories to analyze (Hate, SelfHarm, Sexual, Violence)
    # You can adjust severities as needed, 0-6 are valid, default is 0 for all
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE_CONTENT,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL_CONTENT,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    safety_results = {}
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            safety_results[category_analysis.category.value] = {
                "severity": category_analysis.severity,
                "detected": category_analysis.severity > 0 # Simple heuristic: if severity > 0, it's detected
            }
    return safety_results

if __name__ == "__main__":
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    safe_text = "This is a perfectly normal and safe sentence."
    risky_text = "I hate this, I will hurt myself. This is violent and sexual content."

    print("Checking safe text:")
    try:
        safe_result = check_corpus_safety(safe_text)
        print(safe_result)
    except ValueError as e:
        print(f"Error checking safe text: {e}")

    print("\nChecking risky text:")
    try:
        risky_result = check_corpus_safety(risky_text)
        print(risky_result)
    except ValueError as e:
        print(f"Error checking risky text: {e}")
