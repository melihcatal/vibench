from document_client import DocumentClient, get_project_id
from document_models import SafetyAnalysisRequest, SafetyAnalysisResponse
from google.cloud import language_v1 as language

def ocr_safety(request: SafetyAnalysisRequest) -> SafetyAnalysisResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id)
    client = doc_client_helper.get_language_client()

    document = language.Document(content=request.text, type_=language.Document.Type.PLAIN_TEXT)
    encoding_type = language.EncodingType.UTF8

    try:
        sentiment_response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
        sentiment_score = sentiment_response.document_sentiment.score

        # For content safety, we can look for specific entities or categories
        # This is a simplified example; a real safety check would be more complex
        categories_response = client.classify_text(request={'document': document})
        categories = []
        for category in categories_response.categories:
            categories.append({"name": category.name, "confidence": category.confidence})

        return SafetyAnalysisResponse(
            categories=categories,
            sentiment_score=sentiment_score
        )

    except Exception as e:
        print(f"Error performing safety analysis: {e}")
        return SafetyAnalysisResponse()
