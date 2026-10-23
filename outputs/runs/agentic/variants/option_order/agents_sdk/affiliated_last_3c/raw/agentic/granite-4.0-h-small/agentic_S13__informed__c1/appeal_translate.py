from safety_client import SafetyClient

def translate_appeal(appeal_text: str, target_lang: str = 'en') -> str:
    """Translate an appeal message using Amazon Translate.

    This example uses the same AWS credentials as the moderation client.
    """
    client = SafetyClient()  # re-use AWS configuration
    # Call Comprehend's TranslateText (used for language translation in this example)
    response = client.translate_text(
        Text=appeal_text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_lang
    )
    return response['TranslatedText']
