from google.cloud import language_v1
from document_client import get_google_nlp_credentials
from typing import Dict, Any

def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Google Cloud Natural Language API.
    """
    creds = get_google_nlp_credentials()
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text content for safety
    try:
        moderation_response = client.moderate_text(document=document)
        moderation_results = {"is_safe": True, "categories": []}
        for category in moderation_response.moderation_categories:
            if category.score > 0.7:  # Threshold for flagging content
                moderation_results["is_safe"] = False
            moderation_results["categories"].append({"name": category.name, "score": category.score})
        return moderation_results
    except Exception as e:
        return {"is_safe": False, "categories": [], "error": str(e)}
