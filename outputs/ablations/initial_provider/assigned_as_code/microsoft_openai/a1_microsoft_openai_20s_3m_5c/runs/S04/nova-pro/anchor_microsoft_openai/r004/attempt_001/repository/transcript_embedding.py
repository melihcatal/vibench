import boto3


def transcript_embedding(transcript, config=None):
    config = config or {}
    comprehend_client = boto3.client('comprehend', region_name=config['region'], aws_access_key_id=config.get('api_key') or os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=config.get('secret_key') or os.environ['AWS_SECRET_ACCESS_KEY'])
    response = comprehend_client.detect_sentiment(Text=transcript, LanguageCode='en')
    return {'sentiment': response['Sentiment']}