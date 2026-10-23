import boto3


def translate_log_message(text: str, source_language: str = "en", target_language: str = "es") -> str:
    client = boto3.client("translate")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response.get("TranslatedText", "")


if __name__ == "__main__":
    translate_log_message("sample")
