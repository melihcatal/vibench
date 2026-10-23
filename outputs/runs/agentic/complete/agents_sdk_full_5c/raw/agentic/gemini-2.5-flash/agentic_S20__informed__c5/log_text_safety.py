import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_text_safety(log_message: str):
    """
    Checks selected log message text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Define categories and their desired severities
    # You can adjust the severities based on your requirements (0-6)
    request = AnalyzeTextOptions(
        text=log_message,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        # Optionally set blocklist_names to check against custom blocklists
        # blocklist_names=["my_blocklist"]
    )

    try:
        response = client.analyze_text(request)
        print(f"Content Safety Analysis for log message: '{log_message}'")
        results = {}
        for category_result in response.categories_analysis:
            results[category_result.category.value] = category_result.severity
            print(f"  {category_result.category.value} severity: {category_result.severity}")
        return results
    except Exception as e:
        print(f"Error checking content safety: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables
    test_message_1 = "This is a normal log message."
    check_log_text_safety(test_message_1)

    print("\n---")
    test_message_2 = "I hate this system, it''s terrible!" # Escaped single quote
    check_log_text_safety(test_message_2)

    print("\n---")
    test_message_3 = "Killing processes in the data center."
    check_log_text_safety(test_message_3)
