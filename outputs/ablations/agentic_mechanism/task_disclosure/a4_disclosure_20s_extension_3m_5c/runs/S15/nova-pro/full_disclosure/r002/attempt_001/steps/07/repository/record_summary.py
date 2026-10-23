import boto3

def summarize_text(text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return summary

def record_summary(document):
    text = document.get('text', '')
    summary = summarize_text(text)
    return {
        'document_id': document.get('id'),
        'summary': summary
    }
