from google.cloud import language_v1

def check_annotation_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text content for categories that might indicate unsafe content
    response_classify = client.classify_text(request={'document': document})
    categories = [{'name': category.name, 'confidence': category.confidence} for category in response_classify.categories]

    # Analyze sentiment for potential negative sentiment
    response_sentiment = client.analyze_sentiment(request={'document': document})
    sentiment = {
        'score': response_sentiment.document_sentiment.score,
        'magnitude': response_sentiment.document_sentiment.magnitude
    }

    # Analyze entities for specific keywords that might be unsafe
    response_entities = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
    entities = [{'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name, 'salience': entity.salience} for entity in response_entities.entities]

    is_unsafe = False
    unsafe_reasons = []

    # Simple checks for potential unsafe content based on categories and sentiment
    for category in categories:
        if "/Violence" in category['name'] and category['confidence'] > 0.7:
            is_unsafe = True
            unsafe_reasons.append(f"Content classified as violence with high confidence ({category['confidence']:.2f}).")
        if "/Adult" in category['name'] and category['confidence'] > 0.7:
            is_unsafe = True
            unsafe_reasons.append(f"Content classified as adult with high confidence ({category['confidence']:.2f}).")

    if sentiment['score'] < -0.5 and sentiment['magnitude'] > 1.0:
        is_unsafe = True
        unsafe_reasons.append(f"Strong negative sentiment detected (score: {sentiment['score']:.2f}, magnitude: {sentiment['magnitude']:.2f}).")

    # Example: check for specific keywords (can be expanded)
    unsafe_keywords = ["kill", "attack", "hate", "harm", "threat"]
    if any(keyword in text.lower() for keyword in unsafe_keywords):
        is_unsafe = True
        unsafe_reasons.append("Contains potentially unsafe keywords.")

    return {
        "text": text,
        "is_unsafe": is_unsafe,
        "reasons": unsafe_reasons,
        "categories": categories,
        "sentiment": sentiment,
        "entities": entities
    }
