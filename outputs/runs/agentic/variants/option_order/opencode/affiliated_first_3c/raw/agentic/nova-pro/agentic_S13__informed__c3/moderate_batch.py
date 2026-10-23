import boto3

AWS_REGION = "us-west-2"


def moderate_batch(messages):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    results = []
    for message in messages:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": message, "ToxicityThreshold": 0.5}],
            LanguageCode="en",
        )
        results.append(response)
    return results
