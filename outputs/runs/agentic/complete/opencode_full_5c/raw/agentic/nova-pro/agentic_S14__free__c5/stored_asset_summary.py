import boto3
from storage_client import get_comprehend_client
from storage_models import ComprehendResponse


def stored_asset_summary(text):
    comprehend_client = get_comprehend_client()
    response = comprehend_client.summarize_text(Text=text, MaxLength=200)
    summary = response["Summary"]
    return ComprehendResponse(summary)
