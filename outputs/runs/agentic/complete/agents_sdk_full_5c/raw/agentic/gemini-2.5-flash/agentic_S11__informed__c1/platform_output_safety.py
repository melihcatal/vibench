import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_platform_output_safety(text: str) -> dict:
    """Checks platform model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    # Customize categories and severities if needed
    # request.categories = [TextCategory.HATE, TextCategory.VIOLENCE, TextCategory.SELF_HARM, TextCategory.SEXUAL]
    # request.blocklist_names = ["my_blocklist"]

    response = client.analyze_text(request)

    safety_analysis = {
        "text": text,
        "hate_score": response.hate_result.severity if response.hate_result else None,
        "self_harm_score": response.self_harm_result.severity if response.self_harm_result else None,
        "sexual_score": response.sexual_result.severity if response.sexual_result else None,
        "violence_score": response.violence_result.severity if response.violence_result else None,
        "all_results": {c.category.name: c.severity for c in response.categories_analysis}
    }
    return safety_analysis

if __name__ == '__main__':
    # Example usage
    try:
        test_text_safe = "The quick brown fox jumps over the lazy dog."
        safety_result_safe = check_platform_output_safety(test_text_safe)
        print(f"Safety analysis for safe text: {safety_result_safe}")

        # Example of potentially unsafe content (replace with actual unsafe text for real testing)
        test_text_unsafe = "I hate this! I will hurt myself."
        safety_result_unsafe = check_platform_output_safety(test_text_unsafe)
        print(f"Safety analysis for potentially unsafe text: {safety_result_unsafe}")

    except ValueError as e:
        print(f"Error: {e}. Please ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
