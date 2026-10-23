import boto3
from observability_models import MetricAnnotationRequest


def metric_annotation_safety(request: MetricAnnotationRequest):
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_syntax(Text=request.text, LanguageCode="en")
    unsafe = any(
        token.get("PartOfSpeech", {}).get("Tag") in {"X", "SYM"}
        for token in response.get("SyntaxTokens", [])
    )
    return {"unsafe": unsafe, "text": request.text, "locale": request.locale}
