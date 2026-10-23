import boto3
import os

def translate_text_for_locale(text: str, target_language_code: str, source_language_code: str = "en") -> str:
    client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    
    return response.get("TranslatedText")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # AWS_SECRET_ACCESS_KEY="your-secret-key"
    english_text = "Hello, how are you today?"
    spanish_text = translate_text_for_locale(english_text, "es")
    print(f"English: {english_text}")
    print(f"Spanish: {spanish_text}")

    french_text = translate_text_for_locale("The weather is beautiful.", "fr")
    print(f"English: The weather is beautiful.")
    print(f"French: {french_text}")
