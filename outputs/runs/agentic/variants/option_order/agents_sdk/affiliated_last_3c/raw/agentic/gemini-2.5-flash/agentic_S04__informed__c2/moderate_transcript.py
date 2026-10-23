import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def moderate_transcript_text(text: str) -> dict:
    """
    Moderates a transcript text using Azure AI Content Safety.

    Args:
        text: The text content to moderate.

    Returns:
        A dictionary containing moderation results, including category scores.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Define categories for moderation
    # You can choose specific categories or all available ones
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
        TextCategory.VIOLENCE,
    ]

    request = AnalyzeTextOptions(text=text, categories=categories)
    
    try:
        response = client.analyze_text(request)
        
        moderation_results = {}
        for category_score in response.categories_analysis:
            moderation_results[category_score.category.value.lower()] = {
                "severity": category_score.severity,
                "detected": category_score.severity > 0 # Severity > 0 indicates content was detected in that category
            }
        return moderation_results
    except Exception as e:
        print(f"Error during content moderation with Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    # try:
    #     sample_text_safe = "This is a normal conversation about technology."
    #     sample_text_risky = "I hate you, you are so stupid. I will hurt you!"
    #
    #     print("Moderating safe text:")
    #     results_safe = moderate_transcript_text(sample_text_safe)
    #     print(results_safe)
    #
    #     print("
Moderating risky text:")
    #     results_risky = moderate_transcript_text(sample_text_risky)
    #     print(results_risky)
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass