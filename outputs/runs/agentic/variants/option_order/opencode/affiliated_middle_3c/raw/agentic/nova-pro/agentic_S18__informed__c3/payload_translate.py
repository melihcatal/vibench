import boto3

# Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Translate customer-facing message payload text
def translate_payload(payload, target_language="es"):
    translate = boto3.client(
        "translate",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = translate.translate_text(
        Text=payload, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]


if __name__ == "__main__":
    payload = "Hello, how are you?"
    print(translate_payload(payload))
