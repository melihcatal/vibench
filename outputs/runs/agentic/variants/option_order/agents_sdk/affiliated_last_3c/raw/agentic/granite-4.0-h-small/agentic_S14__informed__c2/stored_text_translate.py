import os
from typing import List
from storage_models import validate_bucket_and_key, normalize_object_info

def stored_text_translate(bucket: str, key: str, target_lang: str = 'es', translator: str = 'deepl'):
    """Translate extracted text from a stored document to another language.

    bucket: S3 bucket containing the text file (or plain text blob)
    key: object key (path) to the text file
    target_lang: ISO language code, e.g., 'fr', 'es'
    translator: identifies the translation provider (defaults to 'deepl')
    Returns the translated text as a string.
    """
    # 1. Load the stored text (assumes the object is plain UTF-8 text)
    import boto3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    validate_bucket_and_key(bucket, key)
    response = s3.get_object(Bucket=bucket, Key=key)
    original_text = response['Body'].read().decode('utf-8')

    # 2. Call translation service SDK
    if translator.lower() == 'deepl':
        from deepl import DeepL
        dl = DeepL(auth_key=os.getenv('DEEPL_AUTH_KEY'))
        # DeepL requires a list of texts; we pass a single element list
        result = dl.translate_text(original_text, target_lang=target_lang)
    elif translator.lower() == 'google-cloud-translate':
        from google.cloud import translate_v2 as translate
        translate_client = translate.Client()
        result = translate_client.translate(original_text, target_language=target_lang)
    elif translator.lower() == 'azure-ai-translation-text':
        from azure.ai.translation.translate import TranslationClient
        from azure.ai.translation.translate.models import TranslationRequestList
        client = TranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=os.getenv('AZURE_TRANSLATOR_KEY'))
        request = TranslationRequestList(
            inputs=[{'Text': original_text, 'TargetLanguage': target_lang}]
        )
        result = client.translate(request)
    else:
        raise ValueError(f'Unsupported translator: {translator}')

    translated_text = result['text'] if isinstance(result, dict) else result[0]['text']
    print(f'Translated {key} to {target_lang} using {translator}')
    return translated_text
