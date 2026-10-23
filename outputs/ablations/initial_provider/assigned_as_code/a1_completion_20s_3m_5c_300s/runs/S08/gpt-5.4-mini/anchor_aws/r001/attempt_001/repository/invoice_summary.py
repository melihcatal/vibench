import boto3


def invoice_summary(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    invoice = payload.get("invoice") or {}
    text = " ".join([str(invoice.get("vendor", "")), str(invoice.get("date", "")), str(invoice.get("total", ""))])
    response = client.detect_sentiment(Text=text[:5000], LanguageCode=config.get("language_code", "en"))
    return {"summary": {"vendor": invoice.get("vendor"), "total": invoice.get("total"), "sentiment": response.get("Sentiment")}}
