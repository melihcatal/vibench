import os
import boto3

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def apply_safety_threshold(text: str, toxicity_threshold: float = 0.8):
    client = boto3.client(
        "comprehend",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    overall_toxicity_score = 0.0
    for result in response.get("ResultList", []):
        for score in result.get("Toxicity", {}).get("Scores", []):
            if score.get("Name") == "Overall":
                overall_toxicity_score = score.get("Score", 0.0)
                break

    if overall_toxicity_score >= toxicity_threshold:
        return {"decision": "DENY", "score": overall_toxicity_score}
    else:
        return {"decision": "ALLOW", "score": overall_toxicity_score}
