import boto3

def collect_platform_metadata():
    sts_client = boto3.client('sts')
    response = sts_client.get_caller_identity()
    account_id = response['Account']
    user_id = response['UserId']
    arn = response['Arn']
    print(f'Account ID: {account_id}')
    print(f'User ID: {user_id}')
    print(f'ARN: {arn}')
    
    # Example of collecting model output and metadata
    comprehend_client = boto3.client('comprehend')
    text = 'Sample text for sentiment analysis.'
    sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentiment_response['Sentiment']
    print(f'Sentiment: {sentiment}')
    
    # Example of collecting usage and resource IDs
    comprehend_usage_response = comprehend_client.describe_dominant_language_detection_job(JobId='example-job-id')
    usage = comprehend_usage_response['DetectDominantLanguageDetectionJobProperties']['InputDataConfig']['S3Uri']
    print(f'Usage: {usage}')
    
if __name__ == '__main__':
    collect_platform_metadata()