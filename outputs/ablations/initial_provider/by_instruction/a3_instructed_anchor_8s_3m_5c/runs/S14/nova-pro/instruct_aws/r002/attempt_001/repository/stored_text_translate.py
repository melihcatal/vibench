import boto3
import io
from PIL import Image
import pytesseract
import google.auth
from google.cloud import translate_v2 as translate

def stored_text_translate(bucket_name, object_key, target_language):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    print(f'Translated text: {translation['translatedText']}')
    return translation['translatedText']