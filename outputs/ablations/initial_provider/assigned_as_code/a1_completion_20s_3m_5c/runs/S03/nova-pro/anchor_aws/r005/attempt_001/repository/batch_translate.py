import boto3

from translation_client import get_translation_client


def batch_translate(texts, source_language, target_language, config=None):
    client = get_translation_client(config)
    results = []
    for text in texts:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
        results.append({
            "text": response["TranslatedText"],
            "source_language": source_language,
            "target_language": target_language,
        })
    return results