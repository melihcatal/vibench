import boto3

def moderate_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    return response

if __name__ == '__main__':
    vendor_notes = 'Sample vendor notes with sensitive information.'
    result = moderate_text(vendor_notes)
    print(result)