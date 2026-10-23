from google.cloud import language_v1

def check_caption_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # This is a basic example. For robust content safety, consider Perspective API or more advanced NLP techniques.
    # Here, we'll just return a simplified safety score based on sentiment magnitude and score.
    safety_score = (sentiment.magnitude * (1 + sentiment.score)) / 2  # Scale to roughly 0-1
    is_unsafe = safety_score < 0.2 # Arbitrary threshold for demonstration

    return {"is_unsafe": is_unsafe, "score": sentiment.score, "magnitude": sentiment.magnitude}
