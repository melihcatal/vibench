import azure.ai.textanalytics as textanalytics


def moderate_claims(text, config):
    client = textanalytics.TextAnalyticsClient(endpoint=config['endpoint'], credential=config['credential'])
    result = client.analyze_sentiment(documents=[text])[0]
    return result.sentiment