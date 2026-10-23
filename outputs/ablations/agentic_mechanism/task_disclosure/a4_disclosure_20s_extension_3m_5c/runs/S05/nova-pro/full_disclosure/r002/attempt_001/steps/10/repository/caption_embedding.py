import boto3

def embed_caption_chunks(caption_chunks):
    comprehend = boto3.client('comprehend')
    embeddings = []
    for chunk in caption_chunks:
        response = comprehend.detect_sentiment(Text=chunk, LanguageCode='en')
        embeddings.append(response['Sentiment'])
    return embeddings