from google.cloud import language_v1

def check_secret_labels_and_notes(secret_labels, secret_notes):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=secret_labels + ' ' + secret_notes, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    if sentiment.score < -0.5:
        return 'Unsafe text detected'
    else:
        return 'Safe text'

if __name__ == '__main__':
    secret_labels = 'example label'
    secret_notes = 'example note'
    result = check_secret_labels_and_notes(secret_labels, secret_notes)
    print(result)