import boto3

def embed_for_search(query, documents):
    client = boto3.client('comprehend')
    query_embedding = client.detect_sentiment(Text=query, LanguageCode='en')['SentimentScore']
    document_embeddings = [client.detect_sentiment(Text=doc, LanguageCode='en')['SentimentScore'] for doc in documents]
    return query_embedding, document_embeddings