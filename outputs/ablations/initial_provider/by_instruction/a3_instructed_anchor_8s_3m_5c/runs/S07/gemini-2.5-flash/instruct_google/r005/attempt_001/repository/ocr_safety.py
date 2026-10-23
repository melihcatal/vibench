from google.cloud import language_v1 as language
from document_models import ExtractedText
from typing import Dict, Any

def check_ocr_safety(extracted_text: ExtractedText) -> Dict[str, Any]:
    """Checks extracted document text for unsafe content using Google Cloud Natural Language API.

    This uses the experimental 'moderate_text' feature available in newer versions of the API for content safety detection.
    """
    client = language.LanguageServiceClient()

    document = language.Document(content=extracted_text.text_content, type_=language.Document.Type.PLAIN_TEXT)

    # Using moderate_text for content safety detection
    # Note: This feature might be in preview or require specific API versions/configurations.
    # For broader safety, other APIs like Perspective API might be considered.
    try:
        response = client.moderate_text(document=document)
        safety_attributes = []
        for sentiment_topic in response.moderation_categories:
            safety_attributes.append({
                "category": sentiment_topic.category,
                "confidence": sentiment_topic.confidence
            })
        return {"safety_scores": safety_attributes}
    except Exception as e:
        return {"error": str(e), "message": "Could not moderate text. Ensure API version and permissions are correct."}

if __name__ == "__main__":
    # Example usage: Replace with your extracted text
    # extracted_text = ExtractedText(text_content="This is a sample text that might contain some unsafe content.")
    # safety_report = check_ocr_safety(extracted_text)
    # print(safety_report)
    pass
