import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

def moderate_text_segment(text: str):
    """Moderates a text segment using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.Hate, TextCategory.SelfHarm, TextCategory.Sexual, TextCategory.Violence],
        blocklist_names=["Default"], # You can define and use blocklists in your Content Safety resource
    )

    try:
        response = client.analyze_text(request)
        print("Content Safety analysis results:")
        for category in response.categories_analysis:
            print(f"  Category: {category.category}, Severity: {category.severity}")
        return response
    except Exception as err:
        print(f"Content Safety analysis failed: {err}")
        return None

if __name__ == "__main__":
    # Example usage
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    # sample_transcript_segment = "I hate this! You are so stupid and I will hurt you."
    # moderation_result = moderate_text_segment(sample_transcript_segment)
    # if moderation_result:
    #     print("\nModeration complete.")
    pass
