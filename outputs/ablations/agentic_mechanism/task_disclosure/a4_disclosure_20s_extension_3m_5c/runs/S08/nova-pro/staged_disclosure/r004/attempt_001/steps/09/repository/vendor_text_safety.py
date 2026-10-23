import boto3

def moderate_vendor_notes(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=text,
        LanguageCode='en'
    )
    return response

# Example usage
vendor_note = 'Example vendor note'
moderation_result = moderate_vendor_notes(vendor_note)
print(moderation_result)