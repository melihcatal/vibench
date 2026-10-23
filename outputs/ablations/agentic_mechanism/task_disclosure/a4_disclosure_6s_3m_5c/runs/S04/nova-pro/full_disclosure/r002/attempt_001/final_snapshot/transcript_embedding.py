import boto3

def embed_transcript_segments(text_segments):
    comprehend = boto3.client('comprehend')
    embeddings = []
    for segment in text_segments:
        response = comprehend.detect_dominant_language(Text=segment)
        if response['Languages'][0]['LanguageCode'] == 'en':
            embed_response = comprehend.detect_sentiment(Text=segment, LanguageCode='en')
            embeddings.append(embed_response['SentimentScore'])
    return embeddings