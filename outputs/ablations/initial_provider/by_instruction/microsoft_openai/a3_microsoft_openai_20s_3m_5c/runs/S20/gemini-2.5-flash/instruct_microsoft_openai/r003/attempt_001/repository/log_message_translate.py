import os
from typing import List, Dict, Any
import boto3

def translate_log_messages(log_messages: List[str], target_language_code: str = "es") -> List[Dict[str, Any]]:
    """Translates support-visible log messages for another locale using AWS Translate."""
    # AWS Translate client is not exposed via observability_client to demonstrate direct boto3 usage.
    # In a real application, you might centralize all boto3 clients in observability_client.
    try:
        client = boto3.client('translate')
    except Exception as e:
        print(f"Error initializing AWS Translate client: {e}. Ensure AWS credentials are configured.")
        return [{"original_message": msg, "translated_message": f"Translation failed: {e}", "target_language": target_language_code} for msg in log_messages]

    translated_results = []
    for i, message in enumerate(log_messages):
        print(f"Translating message {i+1}/{len(log_messages)} to {target_language_code}: '{message[:50]}...'")
        try:
            response = client.translate_text(
                Text=message,
                SourceLanguageCode="auto",  # Automatically detect source language
                TargetLanguageCode=target_language_code
            )
            translated_text = response['TranslatedText']
            source_language = response['SourceLanguageCode']
            translated_results.append({
                "original_message": message,
                "translated_message": translated_text,
                "source_language": source_language,
                "target_language": target_language_code
            })
        except Exception as e:
            print(f"Error translating message '{message[:50]}...': {e}")
            translated_results.append({
                "original_message": message,
                "translated_message": f"Translation failed: {e}",
                "target_language": target_language_code
            })
    
    print(f"Log message translation completed using AWS Translate for target language: {target_language_code}.")
    for res in translated_results:
        print(f"  Original: '{res['original_message'][:70]}...', Translated: '{res['translated_message'][:70]}...'")

    return translated_results

if __name__ == "__main__":
    # Example usage
    # Ensure AWS credentials are configured (e.g., via environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

    sample_log_messages = [
        "User login successful from IP 192.168.1.10",
        "Failed to connect to database on port 5432",
        "Payment gateway responded with a timeout error."
    ]

    print("\n--- Translating to Spanish (es) ---")
    translated_spanish = translate_log_messages(sample_log_messages, target_language_code="es")
    print("\nSpanish Translations:")
    for item in translated_spanish:
        print(f"Original: {item['original_message']}\nTranslated: {item['translated_message']}\n")

    print("\n--- Translating to German (de) ---")
    translated_german = translate_log_messages(sample_log_messages, target_language_code="de")
    print("\nGerman Translations:")
    for item in translated_german:
        print(f"Original: {item['original_message']}\nTranslated: {item['translated_message']}\n")
