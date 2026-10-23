import os
from google.cloud import language_v2
from google.cloud.language_v2 import enums

def summarize_moderation_decision(text_content):
    """
    Summarizes moderation decisions using Google Cloud Natural Language API.
    """
    # Instantiates a client
    client = language_v2.LanguageServiceClient()

    # The text to analyze
    document = {"content": text_content, "type_": enums.Document.Type.PLAIN_TEXT}

    # Available categories: "places", "legal", "harmful", "political", etc.
    # See https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={"document": document})

    summary = {
        "categories": [category.name for category in response.categories]
    }
    return summary

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or
    # provide other authentication methods as per Google Cloud documentation.
    # For local development, you might need to set up authentication:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    text_to_moderate = "This content contains hate speech and is offensive."
    decision_summary = summarize_moderation_decision(text_to_moderate)
    print(f"Moderation Decision Summary: {decision_summary}")

    text_to_moderate_2 = "This is a neutral comment about a product."
    decision_summary_2 = summarize_moderation_decision(text_to_moderate_2)
    print(f"Moderation Decision Summary 2: {decision_summary_2}")
