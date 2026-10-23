from google.cloud import language_v1

def embed_log_message(log_message):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=log_message, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score

if __name__ == '__main__':
    log_message = 'This is a log message'
    print(embed_log_message(log_message))