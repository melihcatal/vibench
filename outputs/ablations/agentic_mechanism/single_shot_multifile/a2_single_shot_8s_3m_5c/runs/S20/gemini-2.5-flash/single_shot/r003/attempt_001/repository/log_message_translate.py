from observability_client import clients
from typing import List

def translate_log_messages(
    log_messages: List[str],
    source_language_code: str = "en",
    target_language_code: str = "es"
) -> List[str]:
    """
    Translates support-visible log messages for another locale using AWS Translate.
    """
    aws_translate_client = clients.aws_translate_client
    
    translated_messages = []
    for message in log_messages:
        try:
            response = aws_translate_client.translate_text(
                Text=message,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code
            )
            translated_messages.append(response["TranslatedText"])
        except Exception as e:
            translated_messages.append(f"Translation Error: {e} for message: '{message}'")
    
    return translated_messages
