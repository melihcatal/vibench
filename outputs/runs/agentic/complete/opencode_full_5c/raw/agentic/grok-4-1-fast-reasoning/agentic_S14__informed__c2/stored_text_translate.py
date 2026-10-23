import boto3
from storage_client import get_s3_client, get_aws_session

def stored_text_translate(bucket: str, key: str, source_language: str = 'en', target_language: str = 'es') -&gt; str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj['Body'].read().decode('utf-8')
    session = get_aws_session()
    translate_client = session.client('translate')
    resp = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return resp['TranslatedText']