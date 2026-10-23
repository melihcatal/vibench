import boto3


def batch_translate(texts, source_lang, target_lang):
    client = boto3.client("translate")
    results = client.translate_batch_text(
        TextTranslationJobs=[
            {
                "SourceLanguageCode": source_lang,
                "TargetLanguageCode": target_lang,
                "Texts": texts,
            }
        ]
    )
    translated_texts = [item["TranslatedText"] for item in results["TranslatedTexts"]]
    return translated_texts
