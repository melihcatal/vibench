import boto3

translate = boto3.client("translate", region_name="us-west-2")


def batch_translate(texts, source_language, target_language):
    results = []
    for text in texts:
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        results.append(result["TranslatedText"])
    return results
