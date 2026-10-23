import boto3


def summarize_image_analysis(analysis_results):
    translate_client = boto3.client("translate")
    summarized_results = {}
    for key, value in analysis_results.items():
        translated_text = translate_client.translate_text(
            Text=str(value), SourceLanguageCode="en", TargetLanguageCode="en"
        )
        summarized_results[key] = translated_text["TranslatedText"]
    return summarized_results
