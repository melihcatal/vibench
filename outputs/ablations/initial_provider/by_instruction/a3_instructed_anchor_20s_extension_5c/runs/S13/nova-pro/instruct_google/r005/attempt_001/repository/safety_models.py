from google.cloud.language_v1 import Document, Sentiment

def create_document(text):
    return Document(content=text, type_=Document.Type.PLAIN_TEXT)

def extract_sentiment(response):
    return response.document_sentiment