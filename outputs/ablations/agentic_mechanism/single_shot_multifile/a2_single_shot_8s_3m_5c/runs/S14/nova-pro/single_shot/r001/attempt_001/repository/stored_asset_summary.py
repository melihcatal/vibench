import boto3

def summarize_text(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    return response

if __name__ == '__main__':
    print(summarize_text('This is a sample text to summarize.'))