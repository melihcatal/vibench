import boto3


def batch_translate(texts, source_lang, target_lang):
    client = boto3.client("translate")
    results = []
    for text in texts:
        result = client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        results.append(result["TranslatedText"])
    return results
