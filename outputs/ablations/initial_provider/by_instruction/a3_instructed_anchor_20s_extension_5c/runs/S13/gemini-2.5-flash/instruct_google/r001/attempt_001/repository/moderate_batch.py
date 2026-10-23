from google.cloud import language_v1
from typing import List
from safety_models import ModerationResult, ModerationScore

def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    client = language_v1.LanguageServiceClient()
    results = []
    
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)
        
        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude
        
        is_flagged_by_sentiment = sentiment_score < -0.5
        
        scores = [ModerationScore(category="sentiment", score=sentiment_score)]
        
        decision_reason = ""
        if is_flagged_by_sentiment:
            decision_reason = "Content flagged due to highly negative sentiment."

        results.append(ModerationResult(
            text=text,
            is_flagged=is_flagged_by_sentiment,
            decision_reason=decision_reason,
            scores=scores,
            provider="Google Cloud Natural Language API"
        ))
            
    return results

