import boto3


def translate_message(message: str, target_language: str = "es") -> dict:
    client = boto3.client("translate")
    response = client.translate_text(Text=message, SourceLanguageCode="en", TargetLanguageCode=target_language)
    return {"provider": "aws-translate", "translated_text": response.get("TranslatedText", "")}


if __name__ == "__main__":
    translate_message("sample")
