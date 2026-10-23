"""
Checks log message text for unsafe content using Azure AI Content Safety.
"""
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_safety(log_message: str):
    """
    Analyzes a log message for harmful content using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Error: AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
        return

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message, categories=[
        TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE
    ])

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return

    print(f"Checking message: '{log_message}'")
    results = {}
    unsafe = False
    for category in response.categories_analysis:
        results[category.category.value] = category.severity
        if category.severity > 0:
            unsafe = True

    if unsafe:
        print("Unsafe content detected.")
        for category, severity in results.items():
            if severity > 0:
                print(f"  - Category: {category}, Severity: {severity}")
    else:
        print("No unsafe content detected.")

if __name__ == "__main__":
    safe_message = "User login failed due to invalid credentials."
    unsafe_message = "i want to attack the server" # Example of potentially harmful text
    check_log_safety(safe_message)
    print("-" * 20)
    check_log_safety(unsafe_message)
