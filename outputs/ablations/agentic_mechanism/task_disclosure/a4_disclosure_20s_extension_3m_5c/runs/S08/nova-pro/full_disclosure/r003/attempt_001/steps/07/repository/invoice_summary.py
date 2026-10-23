import boto3

def summarize_invoice_fields(invoice_fields):
    comprehend = boto3.client('comprehend')
    
    text = ' '.join(invoice_fields.values())
    
    try:
        summary = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        return summary
    except Exception as e:
        print(f"Error summarizing invoice fields: {e}")
        return None