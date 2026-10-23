import boto3

def vendor_text_safety(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(TextSegments=[{'Text': text}])
    return response['ToxicContent'][0]['Labels'][0]['Name'] if response['ToxicContent'] else 'Safe'