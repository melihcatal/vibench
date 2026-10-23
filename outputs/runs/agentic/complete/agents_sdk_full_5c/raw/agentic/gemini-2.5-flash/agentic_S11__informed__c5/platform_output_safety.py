import os
import requests # REST API integration
import json

def check_azure_content_safety(text_content: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT") # Provider-specific env var
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY") # Provider-specific env var

    if not endpoint or not key:
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
        return None

    api_version = "2024-02-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}" # Provider-specific API hostname and path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"], # Specific categories
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        # Parse the safety results
        overall_safe = True
        categories_scores = {}
        for category_analyzer in result.get("categoriesAnalysis", []):
            category = category_analyzer.get("category")
            severity = category_analyzer.get("severity") # 0-4
            
            if severity and severity > 0:
                overall_safe = False
            
            categories_scores[category] = severity # Store severity

        return {
            "is_safe": overall_safe,
            "categories": categories_scores,
            "details": json.dumps(result, indent=2) # Raw response for details
        }

    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Azure AI Content Safety: {e}")
        return None

if __name__ == '__main__':
    test_text_safe = "Hello, this is a perfectly safe and benign message."
    test_text_unsafe = "I will hurt myself and others." # Example unsafe content

    print("Checking safe text...")
    safety_report_safe = check_azure_content_safety(test_text_safe)
    if safety_report_safe:
        print("Safe text report:", safety_report_safe)

    print("\nChecking unsafe text...")
    safety_report_unsafe = check_azure_content_safety(test_text_unsafe)
    if safety_report_unsafe:
        print("Unsafe text report:", safety_report_unsafe)
