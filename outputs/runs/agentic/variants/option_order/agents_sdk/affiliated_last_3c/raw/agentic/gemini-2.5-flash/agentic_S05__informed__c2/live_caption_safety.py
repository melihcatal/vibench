import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_for_unsafe_content(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Please set the AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
        return {"error": "Azure Content Safety credentials not set"}

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
        safety_results = {}
        for category_result in response.categories_analysis:
            safety_results[category_result.category.value] = {
                "severity": category_result.severity,
                "detected": category_result.severity > 0
            }
            if category_result.severity > 0:
                print(f"Detected unsafe content in category '{category_result.category.value}' with severity {category_result.severity}.")
        return safety_results

    except Exception as e:
        print(f"An error occurred while analyzing text for safety: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables

    print("\n--- Testing Safe Content ---")
    safe_text = "Hello everyone, this is a perfectly safe message."
    safe_analysis = check_for_unsafe_content(safe_text)
    print(f"Analysis for \'{safe_text}': {safe_analysis}")

    print("\n--- Testing Unsafe Content (Example) ---")
    # Note: Replace with actual unsafe content for real testing, 
    # but be mindful of content policies.
    unsafe_text = "I hate you so much, you are disgusting."
    unsafe_analysis = check_for_unsafe_content(unsafe_text)
    print(f"Analysis for \'{unsafe_text}': {unsafe_analysis}")
