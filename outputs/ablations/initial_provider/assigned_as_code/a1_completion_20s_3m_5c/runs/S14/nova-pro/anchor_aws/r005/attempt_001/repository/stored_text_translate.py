import boto3
from botocore.exceptions import NoCredentialsError


def translate_stored_text(bucket_name, object_name, target_language):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        file_stream = response['Body']
        # Extract text from the file stream
        # This is a placeholder for the actual text extraction implementation
        text = "Extracted text"
        # Translate the extracted text
        translate = boto3.client('translate')
        result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
        return result.translatedText
    except NoCredentialsError:
        return "Credentials not available"