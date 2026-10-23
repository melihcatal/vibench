import boto3


def translate_log_message(log_text, source_language, target_language):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=log_text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return response.get("TranslatedText")


if __name__ == "__main__":
    print(translate_log_message("This is a test log message.", "en", "es"))
