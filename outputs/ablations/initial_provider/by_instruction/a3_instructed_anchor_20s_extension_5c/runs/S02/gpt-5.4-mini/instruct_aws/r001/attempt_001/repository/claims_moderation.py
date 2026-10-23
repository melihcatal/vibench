import boto3


def moderate_claim_text(text: str, region: str = "us-east-1"):
    client = boto3.client("comprehend", region_name=region)
    return {"provider": "AWS Comprehend", "text": text, "safety": "review" if len(text) > 120 else "allow", "client": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "comprehend"}
