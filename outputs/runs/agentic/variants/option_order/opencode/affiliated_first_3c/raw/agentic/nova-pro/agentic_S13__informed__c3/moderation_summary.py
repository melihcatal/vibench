import boto3

AWS_REGION = "us-west-2"


def moderation_summary(moderation_results):
    translate = boto3.client("translate", region_name=AWS_REGION)
    summary = ""
    for result in moderation_results:
        if result["toxic_content_list"]:
            summary += f"Text: {result['text']}, Toxicity: {result['toxic_content_list'][0]['toxicity']}\n"
    return summary
