import boto3

comprehend = boto3.client('comprehend')

def redact_unsafe(text):
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    redacted_text = text
    for entity in response['Entities']:
        if entity['Type'] in ['BANK_ACCOUNT_NUMBER', 'CREDIT_DEBIT_NUMBER', 'PASSPORT_NUMBER']:
            redacted_text = redacted_text.replace(entity['Text'], '[REDACTED]')
    return redacted_text