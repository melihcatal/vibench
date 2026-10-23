import os
import boto3
from storage_client import get_s3_client
from storage_models import normalize_head_params

def translate_stored_text(bucket, key, target_language='es'):
    """Translates text extracted from a stored document using Amazon Translate.
    Downloads the file, extracts plain text, translates it, and returns the translation.
    """
    # Get S3 client for possible temporary download if needed (here we just treat key as source text)
    s3 = get_s3_client()
    # Assume the stored object is plain text for demo purposes
    # Download to temporary location
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
        s3.download_file(bucket, key, tmp_file.name)
        print(f'Downloaded {key} for translation.')
        source_text = open(tmp_file.name, 'r', encoding='utf-8').read()
        os.unlink(tmp_file.name)
    # Call Translate API
    response = translate_call(source_text, target_language)
    translated_text = response['TranslatedText']
    print(f'Translated text ({len(translated_text)} chars) to language {target_language}.')
    return translated_text

def translate_call(source_text, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=source_text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )
    return response
