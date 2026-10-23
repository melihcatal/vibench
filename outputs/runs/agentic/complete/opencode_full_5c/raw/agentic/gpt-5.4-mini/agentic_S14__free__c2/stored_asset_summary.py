import boto3

from storage_models import SummaryResponse


def stored_asset_summary(text: str, region_name: str = None) -> SummaryResponse:
    client = boto3.client("comprehend", region_name=region_name)
    result = client.detect_key_phrases(Text=text[:5000], LanguageCode="en")
    phrases = [
        item.get("Text") for item in result.get("KeyPhrases", []) if item.get("Text")
    ]
    summary = "; ".join(phrases[:10])
    return SummaryResponse(text=summary, raw=result)
