import boto3



def translate_compliance_notes(payload: Dict[str, Any], config=None) -> Dict[str, Any]:
    config = config or {}
    client = boto3.client('translate', region_name=config.get('region'))
    source_language_code = config.get('source_language_code')
    target_language_code = config.get('target_language_code')
    compliance_notes = payload.get('compliance_notes', '')
    response = client.translate_text(Text=compliance_notes, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    translated_notes = response['TranslatedText']
    return {'translated_notes': translated_notes}
