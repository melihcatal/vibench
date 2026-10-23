import boto3

def claims_moderation(claims):
    comprehend = boto3.client('comprehend')
    moderated_claims = []
    for claim in claims:
        response = comprehend.detect_sentiment(Text=claim, LanguageCode='en')
        if response['Sentiment']!= 'NEGATIVE':
            moderated_claims.append(claim)
    return moderated_claims