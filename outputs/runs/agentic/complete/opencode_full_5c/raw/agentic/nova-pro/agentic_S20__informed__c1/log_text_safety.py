import boto3


def log_text_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(TextSegments=[{"Text": text}])
    for result in response["Results"]:
        print(result["Toxicity"])
    print(f"Checked text safety")
