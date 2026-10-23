from google.cloud import language_v2

def check_payload(text):
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    if response.document_sentiment.score < -0.2:
        return 'Unsafe content detected'
    else:
        return 'Safe content'

if __name__ == '__main__':
    sample_text = 'This is a sample text to check for unsafe content.'
    result = check_payload(sample_text)
    print(result)