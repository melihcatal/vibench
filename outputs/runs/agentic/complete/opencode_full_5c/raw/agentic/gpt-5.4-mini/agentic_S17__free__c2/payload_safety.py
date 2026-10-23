import os
from google.cloud import language_v1

def payload_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    doc = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": doc}).document_sentiment
    unsafe = sentiment.score < -0.5
    return {"unsafe": unsafe, "score": sentiment.score}

if __name__ == '__main__':
    print(payload_safety(os.getenv('PLAINTEXT', '')))
