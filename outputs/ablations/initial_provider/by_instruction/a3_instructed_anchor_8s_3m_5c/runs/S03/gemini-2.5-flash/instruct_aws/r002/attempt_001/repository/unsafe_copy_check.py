import boto3

def unsafe_copy_check(text: str, language_code: str) -> list[dict]:
    """
    Checks localized copy for unsafe content using AWS Comprehend Moderation.
    """
    comprehend = boto3.client("comprehend")
    
    try:
        response = comprehend.detect_toxic_content(
            TextContent={'Text': text},
            LanguageCode=language_code
        )
        return response.get('Result', {}).get('Labels', [])
    except comprehend.exceptions.UnsupportedLanguageException:
        return [{'Message': f'Language {language_code} is not supported for toxic content detection.'}]
    except Exception as e:
        return [{'Error': str(e)}]
