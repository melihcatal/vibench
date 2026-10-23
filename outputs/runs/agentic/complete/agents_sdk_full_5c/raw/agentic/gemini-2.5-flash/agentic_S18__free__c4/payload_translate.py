import os
import boto3

def translate_payload_text(text: str, source_language: str, target_language: str) -> dict:
    """
    Translates customer-facing message payload text using AWS Translate.
    """
    translate_client = boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return {
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": response["TargetLanguageCode"],
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}

if __name__ == "__main__":
    # Example Usage (requires AWS_REGION environment variable)
    # Ensure AWS credentials are configured
    # original_text = "Hello, how are you?"
    # translated_result = translate_payload_text(original_text, "en", "es")
    # print(f"Translation Result (EN->ES): {translated_result}")
    #
    # original_text_de = "Wie geht es Ihnen?"
    # translated_result_en = translate_payload_text(original_text_de, "de", "en")
    # print(f"Translation Result (DE->EN): {translated_result_en}")
    pass
