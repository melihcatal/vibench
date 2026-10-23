import boto3
import translate


def translate_text_from_stored_document(object_name, target_language, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region'))
    response = client.get_object(Bucket=config['bucket'], Key=object_name)
    document_content = response['Body'].read()
    text = document_content.decode('utf-8')
    translator = translate.Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text