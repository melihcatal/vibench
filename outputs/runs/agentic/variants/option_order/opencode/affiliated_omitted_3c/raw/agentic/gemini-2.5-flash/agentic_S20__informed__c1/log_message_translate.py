from observability_client import ObservabilityClient
import os
from typing import List, Dict, Any


def translate_log_messages(
    log_messages: List[str], target_language: str, source_language: str = "en"
) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    translated_messages = []

    if not log_messages:
        return translated_messages

    print(
        f"Translating {len(log_messages)} log messages from {source_language} to {target_language} using Amazon Translate..."
    )

    for i, message in enumerate(log_messages):
        try:
            response = client.translate_text(
                text=message,
                source_language_code=source_language,
                target_language_code=target_language,
            )
            translated_text = response["TranslatedText"]
            translated_messages.append(
                {
                    "original_message": message,
                    "translated_message": translated_text,
                    "source_language": source_language,
                    "target_language": target_language,
                }
            )
            print(f"  Message {i + 1} translated: {translated_text}")
        except Exception as e:
            translated_messages.append({"original_message": message, "error": str(e)})
            print(f"  Error translating message {i + 1}: {e}")

    print("Log message translation completed.")
    return translated_messages


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1

    sample_log_messages = [
        "User 'johndoe' logged in successfully.",
        "Error: Failed to connect to critical service, system might be unstable!",
        "Payment gateway responded with a 404 error.",
        "New order received with ID: ORD-789.",
    ]

    print("\nTranslating to Spanish (es):")
    spanish_translations = translate_log_messages(
        sample_log_messages, target_language="es"
    )
    for trans in spanish_translations:
        print(json.dumps(trans, indent=2))

    print("\nTranslating to German (de):")
    german_translations = translate_log_messages(
        sample_log_messages, target_language="de"
    )
    for trans in german_translations:
        print(json.dumps(trans, indent=2))
