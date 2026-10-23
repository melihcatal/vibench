from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

text = 'your text here'
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
response = client.analyze_sentiment(request={'document': document})
print(response.document_sentiment)