import boto3

def redact_unsafe(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    redacted_text = text
    for entity in response['Entities']:
        if entity['Type'] in ['BANK_ACCOUNT_NUMBER', 'CREDIT_DEBIT_NUMBER', 'PASSPORT_NUMBER']:
            redacted_text = redacted_text.replace(entity['Text'], '[REDACTED]')
    return redacted_text

if __name__ == '__main__':
    sample_text = 'My credit card number is 1234-5678-9012-3456 and my bank account number is 9876543210.'
    print(redact_unsafe(sample_text))