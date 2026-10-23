import os
import boto3

def translate_platform_output(text: str, target_language_code: str = "es") -> dict:
    """
    Translates platform model output for another locale using Amazon Translate.
    """
    translate_client = boto3.client(
        service_name="translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode="auto", # Automatically detect source language
            TargetLanguageCode=target_language_code
        )
        return response
    except Exception as e:
        print(f"Error translating text with Amazon Translate: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    english_text = "Hello, how are you today? The weather is nice."
    
    print("Translating to Spanish:")
    spanish_translation = translate_platform_output(english_text, target_language_code="es")
    print(spanish_translation)

    print("
Translating to French:")
    french_translation = translate_platform_output(english_text, target_language_code="fr")
    print(french_translation)
