import boto3


def batch_translate(texts, source_lang, target_lang):
    client = boto3.client("translate")
    translated_texts = []
    for text in texts:
        response = client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        translated_texts.append(response["TranslatedText"])
    return translated_texts
