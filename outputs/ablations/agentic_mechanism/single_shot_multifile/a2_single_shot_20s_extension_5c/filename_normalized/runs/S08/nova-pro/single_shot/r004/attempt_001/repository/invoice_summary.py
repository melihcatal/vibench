import boto3

def invoice_summary(document_path):
    comprehend = boto3.client('comprehend')
    with open(document_path, 'rb') as document:
        response = comprehend.detect_dominant_language(Text=document.read().decode('utf-8'))
    lang_code = response['Languages'][0]['LanguageCode']
    summary = comprehend.detect_sentiment(Text=document.read().decode('utf-8'), LanguageCode=lang_code)
    return summary['Sentiment']