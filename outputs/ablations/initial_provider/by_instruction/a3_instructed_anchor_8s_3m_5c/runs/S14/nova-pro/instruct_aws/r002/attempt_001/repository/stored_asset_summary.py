import boto3
import io
from PIL import Image
import pytesseract
import spacy

def stored_asset_summary(bucket_name, object_key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    summary = ' '.join([sent.text for sent in doc.sents[:3]])
    print(f'Summary: {summary}')
    return summary