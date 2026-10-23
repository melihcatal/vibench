import boto3

def summarize_document(document_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=document_text,
        LanguageCode='en'
    )
    return response['Sentiment']

if __name__ == '__main__':
    document_text = 'Sample document text to summarize.'
    sentiment = summarize_document(document_text)
    print(f'The sentiment of the document is: {sentiment}')