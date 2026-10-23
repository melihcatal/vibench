from google.cloud import language_v1

def summarize_moderation_decisions(decisions):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content='\n'.join(decisions), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score