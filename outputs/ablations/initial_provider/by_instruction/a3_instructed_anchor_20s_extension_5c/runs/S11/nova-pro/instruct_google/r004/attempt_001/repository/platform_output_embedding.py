import os
from google.cloud import language_v1 as language

def embed_output(project_id, text):
    client = language.LanguageServiceClient(project=project_id)
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    sentiment = analysis.document_sentiment
    return sentiment.score

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    text = 'Hello, world!'
    sentiment_score = embed_output(project_id, text)
    print(sentiment_score)