import boto3

def stored_text_translate(bucket: str, key: str, source_language: str = 'en', target_language: str = 'fr') -> str:
    """
    Translates text extracted from a stored document using Amazon Translate.
    Assumes the stored object is a UTF-8 text file.
    """
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    text = response['Body'].read().decode('utf-8')
    
    translate_client = boto3.client('translate')
    translated = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return translated['TranslatedText']