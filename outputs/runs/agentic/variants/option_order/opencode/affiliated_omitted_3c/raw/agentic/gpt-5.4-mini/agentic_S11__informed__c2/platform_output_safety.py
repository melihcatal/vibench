import boto3


def platform_output_safety(text: str):
    client = boto3.client("comprehend")
    resp = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
    scores = resp.get("ResultList", [])
    return {
        "unsafe": any(item.get("Toxicity", {}).get("Labels") for item in scores),
        "provider": "Amazon Comprehend",
    }
