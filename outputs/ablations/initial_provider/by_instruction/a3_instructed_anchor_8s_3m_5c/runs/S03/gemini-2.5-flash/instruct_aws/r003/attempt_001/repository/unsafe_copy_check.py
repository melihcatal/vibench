import boto3

def unsafe_copy_check(text: str, language_code: str) -> dict:
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_pii_entities(
        Text=text,
        LanguageCode=language_code
    )
    return {
        "pii_entities": response['Entities']
    }
