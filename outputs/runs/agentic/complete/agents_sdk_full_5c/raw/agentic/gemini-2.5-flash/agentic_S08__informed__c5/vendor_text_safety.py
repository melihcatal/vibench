import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_vendor_notes(text_content: str) -> dict:
    """
    Moderates vendor notes or memo fields using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
        return {"error": "Azure Content Safety credentials not configured."}

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_content)

    # By default, all categories are enabled. You can select specific categories if needed.
    # request.categories = [
    #     TextCategory.HATE,
    #     TextCategory.VIOLENCE,
    #     TextCategory.SELF_HARM,
    #     TextCategory.SEXUAL
    # ]
    
    # You can also set a severity level threshold. Default is 0. Lower numbers mean more sensitive detection.
    # request.output_type = AnalyzeTextOutputType.HARM_CATEGORIES

    try:
        response = client.analyze_text(request)
        moderation_results = {"categories_analysis": []}
        for category in response.categories_analysis:
            moderation_results["categories_analysis"].append({
                "category": category.category.value,
                "severity": category.severity # 0-7, 0 being safe, 7 being most severe
            })
        return moderation_results
    except Exception as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    sample_vendor_note_safe = "This invoice covers the consulting services for Q3 2023."
    sample_vendor_note_unsafe = "I hate this company and want to destroy it."

    if not os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT") or not os.environ.get("AZURE_CONTENT_SAFETY_KEY"):
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    else:
        print("Moderating safe vendor note...")
        safe_result = moderate_vendor_notes(sample_vendor_note_safe)
        print("Safe Note Moderation Result:", safe_result)

        print("\nModerating potentially unsafe vendor note...")
        unsafe_result = moderate_vendor_notes(sample_vendor_note_unsafe)
        print("Unsafe Note Moderation Result:", unsafe_result)
