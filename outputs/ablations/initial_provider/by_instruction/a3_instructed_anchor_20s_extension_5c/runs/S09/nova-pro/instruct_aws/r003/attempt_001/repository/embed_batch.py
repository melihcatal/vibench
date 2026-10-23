import boto3

def generate_batch_embeddings(texts):
    client = boto3.client('comprehend')
    embeddings = []
    for text in texts:
        response = client.detect_sentiment(Text=text, LanguageCode='en')
        embedding = response['SentimentScore']
        embeddings.append(embedding)
    return embeddings