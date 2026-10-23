import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def moderate_vendor_notes(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type="FourSeverityLevels"
    )

    try:
        response = client.analyze_text(request)
        result = {}
        for category_result in response.categories_analysis:
            result[category_result.category.value] = {
                "severity": category_result.severity
            }
        return result
    except Exception as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # vendor_note_1 = "This payment covers standard consulting fees."
    # moderation_result_1 = moderate_vendor_notes(vendor_note_1)
    # print(f"Moderation Result for '{vendor_note_1}': {moderation_result_1}")
    #
    # vendor_note_2 = "I hate this company and want to ruin them!"
    # moderation_result_2 = moderate_vendor_notes(vendor_note_2)
    # print(f"Moderation Result for '{vendor_note_2}': {moderation_result_2}")
    pass
