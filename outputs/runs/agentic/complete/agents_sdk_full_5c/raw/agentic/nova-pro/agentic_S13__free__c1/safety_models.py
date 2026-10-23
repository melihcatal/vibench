def classify_text(client, text):
    document = {'content': text, 'type_': 'PLAIN_TEXT'}
    response = client.analyze_sentiment(request={'document': document})
    return {'score': response.document_sentiment.score, 'unsafe': response.document_sentiment.score < -0.25}