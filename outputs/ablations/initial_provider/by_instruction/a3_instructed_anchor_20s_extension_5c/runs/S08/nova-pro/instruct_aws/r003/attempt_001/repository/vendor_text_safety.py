import boto3

def moderate_vendor_notes(vendor_notes):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{'Text': vendor_notes}]
    )
    return response['Results'][0]['Toxicity']