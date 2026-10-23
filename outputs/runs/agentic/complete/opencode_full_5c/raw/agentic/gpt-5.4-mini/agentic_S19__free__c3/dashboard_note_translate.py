import boto3
from observability_models import MetricAnnotationRequest


def dashboard_note_translate(request: MetricAnnotationRequest):
    client = boto3.client("translate", region_name="us-east-1")
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode="auto",
        TargetLanguageCode=request.locale or "en",
    )
    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_text": request.text,
        "locale": request.locale,
    }
