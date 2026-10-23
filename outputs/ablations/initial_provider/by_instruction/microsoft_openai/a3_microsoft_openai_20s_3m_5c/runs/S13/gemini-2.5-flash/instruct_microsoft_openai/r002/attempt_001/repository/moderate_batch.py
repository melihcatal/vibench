import os
import boto3

def moderate_batch(texts: list[str]):
    """
    Moderates a batch of user messages and returns per-message decisions using AWS Comprehend.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    comprehend = boto3.client("comprehend", region_name=region_name)

    # AWS Comprehend does not have a direct "moderation" API like Azure/OpenAI.
    # For content safety, one might typically use PII detection, sentiment analysis, or custom entity recognition.
    # For this example, we'll use PII detection as a proxy for identifying sensitive content.
    # In a real scenario, a custom classification model or an integration with AWS Rekognition for image/video
    # content or a partner solution for text moderation would be used.

    results = []
    for text in texts:
        try:
            response = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
            pii_entities = response.get("Entities", [])
            is_unsafe = len(pii_entities) > 0 # Simple heuristic: presence of PII makes it "unsafe"
            results.append({"text": text, "is_unsafe": is_unsafe, "pii_entities": pii_entities})
        except Exception as e:
            results.append({"text": text, "error": str(e)})
    return results
