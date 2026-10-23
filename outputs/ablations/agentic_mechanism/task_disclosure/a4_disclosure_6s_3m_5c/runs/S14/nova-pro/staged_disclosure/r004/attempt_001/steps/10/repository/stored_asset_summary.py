import boto3

def summarize_asset_content(text):
    comprehend = boto3.client('comprehend')

    # Detect sentiment
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentiment_response['Sentiment']

    # Detect key phrases
    key_phrases_response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    key_phrases = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]

    summary = {
        'sentiment': sentiment,
        'key_phrases': key_phrases
    }

    return summary
