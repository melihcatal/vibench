from google.cloud import language_v2 as language
import os

def check_script_safety(text, project_id=None):
    if not project_id:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    
    client = language.LanguageServiceClient()

    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    
    try:
        response = client.classify_text(document=document)
        safety_categories = []
        for category in response.categories:
            safety_categories.append({
                "name": category.name,
                "confidence": category.confidence
            })
        return {"safety_scores": safety_categories}
    except Exception as e:
        sentiment_response = client.analyze_sentiment(document=document)
        sentiment = sentiment_response.document_sentiment
        return {
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "message": "Classify text failed or not applicable, returned sentiment analysis as an indicator of safety."
        }