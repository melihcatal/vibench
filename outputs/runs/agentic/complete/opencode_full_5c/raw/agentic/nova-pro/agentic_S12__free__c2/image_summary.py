import boto3


def summarize_analysis(labels, text_detections, moderation_labels):
    client = boto3.client("translate")
    summary = "Labels: " + ", ".join(labels) + "\n"
    summary += "Text: " + ", ".join(text_detections) + "\n"
    summary += "Moderation Labels: " + ", ".join(moderation_labels) + "\n"
    response = client.translate_text(
        Text=summary, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
