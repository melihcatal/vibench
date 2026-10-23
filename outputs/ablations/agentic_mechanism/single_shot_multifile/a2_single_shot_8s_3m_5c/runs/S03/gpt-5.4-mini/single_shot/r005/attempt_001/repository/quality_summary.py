from google.cloud import language_v1


def quality_summary(text, locale='en'):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=locale)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    issues = []
    if sentiment.score < -0.25:
        issues.append('negative_tone')
    if len(text.strip()) == 0:
        issues.append('empty_output')
    if any(token in text.lower() for token in ['??', '!!!', 'TODO']):
        issues.append('formatting_or_placeholder_issue')
    return {'score': float(getattr(sentiment, 'score', 0.0)), 'magnitude': float(getattr(sentiment, 'magnitude', 0.0)), 'issues': issues}
