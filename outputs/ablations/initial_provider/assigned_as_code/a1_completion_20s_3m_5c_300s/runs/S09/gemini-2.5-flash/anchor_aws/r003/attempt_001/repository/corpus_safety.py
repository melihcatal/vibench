from google.cloud import language_v2
import os

def corpus_safety(payload, config=None):
    config = config or {}
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    client = language_v2.LanguageServiceClient()

    texts_to_check = payload["texts"]
    safety_results = []

    for text_content in texts_to_check:
        document = language_v2.Document(
            content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
        )
        # Using analyzeSentiment as a proxy for content safety. 
        # For actual content safety, Google Cloud offers more specific APIs like Content Safety API.
        # This is a placeholder for demonstration purposes within the constraints.
        response = client.analyze_sentiment(document=document)
        sentiment = response.document_sentiment
        
        is_safe = True
        safety_score = (sentiment.score + 1) / 2 # Normalize score to 0-1 range

        # A very basic heuristic: if sentiment is too negative, consider it potentially unsafe for some contexts
        if sentiment.score < -0.5: 
            is_safe = False

        safety_results.append({
            "text": text_content,
            "is_safe": is_safe,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude
        })

    return {"safety_checks": safety_results}
