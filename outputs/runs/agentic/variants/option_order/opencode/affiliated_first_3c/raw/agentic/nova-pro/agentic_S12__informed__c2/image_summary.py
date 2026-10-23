import boto3


def summarize_visual_analysis(labels, description, text, safety):
    client = boto3.client("translate")
    translated_description = client.translate_text(
        Text=description, SourceLanguageCode="en", TargetLanguageCode="es"
    )["TranslatedText"]
    summary = f"Labels: {labels}, Description: {translated_description}, Text: {text}, Safety: {safety}"
    return summary
