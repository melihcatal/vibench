import boto3

def summarize_document(document_text):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    response = comprehend.detect_sentiment(
        Text=document_text,
        LanguageCode='en'
    )
    return response['Sentiment']

if __name__ == '__main__':
    document_text = 'This is a sample document text to be summarized.'
    sentiment = summarize_document(document_text)
    print(f'Document sentiment: {sentiment}')
