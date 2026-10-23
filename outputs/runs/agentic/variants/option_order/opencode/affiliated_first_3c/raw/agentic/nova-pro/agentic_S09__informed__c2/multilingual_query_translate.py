import boto3


def multilingual_query_translate(query, target_language):
    client = boto3.client("translate")
    response = client.translate_text(
        Text=query, SourceLanguageCode="auto", TargetLanguageCode=target_language
    )
    return response["TranslatedText"]
