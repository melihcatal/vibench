import boto3


def multilingual_query_translate(query, target_language_code):
    client = boto3.client("translate")
    return client.translate_text(Text=query, SourceLanguageCode="auto", TargetLanguageCode=target_language_code)["TranslatedText"]
