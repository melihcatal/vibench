import boto3

def translate_log_message(
    text: str,
    target_language: str,
    source_language: str = "auto"
) -> str:
    """
    Translates support-visible log messages for another locale using Amazon Translate.

    Args:
        text: The log message to translate.
        target_language: The language code of the target locale (e.g., 'fr', 'es').
        source_language: The language code of the source text ('auto' for detection).

    Returns:
        The translated log message.
    """
    try:
        # Boto3 will use credentials from the environment (AWS_ACCESS_KEY_ID, etc.)
        # or an EC2 instance role.
        translate_client = boto3.client("translate")

        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        return response.get("TranslatedText", "Translation failed.")
    except Exception as e:
        print(f"An error occurred with Amazon Translate: {e}")
        return f"Error during translation: {e}"

# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     original_message = "Warning: User password will expire in 3 days."
#     translated_message = translate_log_message(original_message, target_language="es")
#     print(f"Original: {original_message}")
#     print(f"Translated (Spanish): {translated_message}")
