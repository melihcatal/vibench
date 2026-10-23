import os
import boto3


def record_translate(text, target_language):
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]


if __name__ == "__main__":
    translated_text = record_translate("example text", "es")
    print(translated_text)
